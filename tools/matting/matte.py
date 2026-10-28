"""기존 잘라낸 모양(cut9)을 바탕으로 가장자리를 다시 계산한다.
- 확실한 안/밖 사이 띠에서, 흰 바탕과 섞인 비율(알파)을 색으로 다시 구하고 물건 색만 남긴다(흰 테두리 제거).
- 바닥 쪽에 남은 연한 회색 그림자 얼룩을 지운다(흰 물건 제외)."""
import json,os,sys
import numpy as np
from PIL import Image,ImageFilter
from scipy import ndimage
B=json.load(open('cut9/_boxes.json'))
WHITE=set('boatOrange boatBlue boatPurple dock rockBig rockMid rockSmall buoy fish snowmanRed snowmanBlue snowmanGreen snowballs snowBush shellWhite gull igloo fenceWhite puffA puffB puffC moonFull cabinRed cabinBrown cabinGreen pineSnowA pineSnowB pineSnowC iceBlue icePurple gemPurple gemBlue gemPink sled penguin observatory castleLilac lighthouse'.split())
NOHOLE=set('umbrellaRed umbrellaBlue umbrellaYellow swimRing kite crab owlPost starfishOrange starfishPink bucketBlue bucketGreen hayBale sandcastle'.split())
SKY=set('sun moonCrescent moonFull starWish starBig planetRing planetSmall gull shellWhite'.split())
def refine(n):
    s,y0,y1,x0,x1=B[n]
    src=np.asarray(Image.open(s+'.png').convert('RGB')).astype(float)
    C=src[y0:y1,x0:x1]
    cut=Image.open(f'cut9/{n}.png').convert('RGBA')
    # cut9 는 bbox 로 잘려 있으니 원래 상자 안 위치를 다시 찾는다
    a_cut=np.asarray(cut)[...,3]>128
    full=np.zeros(C.shape[:2],bool)
    # 템플릿 위치: cut9 는 상자에서 alpha bbox 로 crop 됨 → 상자 내 같은 크기 영역을 색 일치로 찾음
    ch,cw=a_cut.shape;best=None
    rgb=np.asarray(cut)[...,:3].astype(float)
    for oy in range(0,C.shape[0]-ch+1):
        for ox in [None]:
            pass
    # 빠르게: 상자 안에서 바탕이 아닌 곳의 bbox 와 크기가 거의 같다 → 바탕 아닌 픽셀 bbox 기준 정렬
    lum=C.mean(2);sat=C.max(2)-C.min(2)
    nb=~((lum>246)&(sat<8))
    ys,xs=np.where(nb)
    cands=[]
    for oy in range(max(0,ys.min()-6),min(C.shape[0]-ch,ys.min()+6)+1):
        for ox in range(max(0,xs.min()-6),min(C.shape[1]-cw,xs.min()+6)+1):
            d=np.abs(C[oy:oy+ch,ox:ox+cw][a_cut]-rgb[a_cut]).mean()
            cands.append((d,oy,ox))
    d,oy,ox=min(cands)
    full[oy:oy+ch,ox:ox+cw]=a_cut
    M=full
    bg=np.median(np.concatenate([C[0],C[-1],C[:,0],C[:,-1]]),axis=0)
    fg=ndimage.binary_erosion(M,iterations=3)
    out=~ndimage.binary_dilation(M,iterations=2)
    band=~fg&~out
    # 띠 안 물건 색 추정: 가장 가까운 확실한 안쪽 색
    _,(iy,ix)=ndimage.distance_transform_edt(~fg,return_indices=True)
    F=C[iy,ix]
    num=((C-bg)*(F-bg)).sum(2);den=((F-bg)**2).sum(2)
    a=np.where(den>200,np.clip(num/np.maximum(den,1e-6),0,1),M.astype(float))
    alpha=np.where(fg,1.0,np.where(out,0.0,a))
    # 흰 물건이 아니면: 바닥 쪽 연한 회색 얼룩 제거
    if n not in WHITE:
        h=C.shape[0];yy=np.arange(h)[:,None]*np.ones(C.shape[1])[None,:]
        ys2=np.where(M.any(1))[0];bot=ys2.max();top=ys2.min()
        greyish=(sat<22)&(lum>190)&(yy>top+(bot-top)*.68)&(alpha>0)
        lab,_=ndimage.label(greyish)
        edge=M&~ndimage.binary_erosion(M,iterations=2)
        hit=set(np.unique(lab[edge&greyish]))-{0}
        rm=np.isin(lab,list(hit))
        alpha=np.where(rm,0,alpha)
    # 해·달·별·갈매기·흰 조개: 아래쪽 연한 얼룩(원래 그림의 그림자·빛 번짐) 지우기
    if n in SKY:
        h=C.shape[0];yy=np.arange(h)[:,None]*np.ones(C.shape[1])[None,:]
        ys2=np.where(M.any(1))[0];bot=ys2.max();top=ys2.min()
        smear=(lum>226)&(sat<(46 if n not in ('gull','shellWhite','moonFull') else 10))&(yy>top+(bot-top)*.62)&(alpha>0)
        lab,_=ndimage.label(smear);edge=M&~ndimage.binary_erosion(M,iterations=2)
        hit=set(np.unique(lab[edge&smear]))-{0}
        alpha=np.where(np.isin(lab,list(hit)),0,alpha)
    # 안쪽 구멍(풍차 날개 격자, 울타리 틈 등)에 남은 흰 바탕을 뚫기
    if (n not in WHITE and n not in NOHOLE) or n=='fenceWhite':
        hole=(lum>(249 if n=='fenceWhite' else 246))&(sat<(6 if n=='fenceWhite' else 8))&(alpha>0)
        labh,kh=ndimage.label(hole)
        if kh:
            sz=ndimage.sum(hole,labh,range(1,kh+1))
            big=np.isin(labh,[i+1 for i,v in enumerate(sz) if v>=18])
            big=ndimage.binary_dilation(big,iterations=1)&(lum>238)&(sat<12)
            alpha=np.where(big,0,alpha)
    if n not in WHITE:
        halo=(alpha<0.6)&(lum>232)&(sat<14)&~fg
        alpha=np.where(halo,0,alpha)
    # 색: 띠는 바탕을 걷어낸 색(F), 안쪽은 원래 색
    col=np.where(band[...,None],F,C)
    # 작은 구멍·튀는 점 정리 + 아주 살짝 부드럽게
    A=Image.fromarray((alpha*255).clip(0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(.6))
    im=Image.fromarray(col.clip(0,255).astype('uint8')).convert('RGBA');im.putalpha(A)
    bb=A.point(lambda v:255 if v>10 else 0).getbbox()
    return im.crop(bb)
OUT=os.environ.get('OUT','cut10')
if __name__=='__main__':
    os.makedirs(OUT,exist_ok=True)
    names=sys.argv[1].split(',') if len(sys.argv)>1 else [k for k in B]
    for n in names:
        refine(n).save(f'{OUT}/{n}.png')
    print(len(names))
