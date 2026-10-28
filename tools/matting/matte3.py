"""누끼 3차: 트라이맵 → 색 분리(언믹싱) 알파 → 가이디드 필터로 경계 다듬기 → 흰 테두리 색 걷어내기."""
import inspect,json,os,sys,re
import numpy as np, cv2
from PIL import Image
from scipy import ndimage
import cut, matte
SRC=inspect.getsource(cut.cutout)
SRC=SRC[:SRC.index("    alpha=Image.fromarray((obj*255)")]+"    return obj,a\n"
SRC=SRC.replace("def cutout(","def maskof(")
exec(SRC,cut.__dict__);maskof=cut.maskof
WHITE,NOHOLE,SKY=matte.WHITE,matte.NOHOLE,matte.SKY
cut.OPT['lighthouse']=dict(thr=1.6,lum=251,sat=6,close=8,peel=0)
cut.OPT['swimRing']=dict(thr=1.6,lum=251,sat=6,close=10,peel=0)
ITEMS={k:tuple(v) for k,v in json.load(open('cut9/_boxes.json')).items()}
SEA={'boatOrange':(92,628,28,398),'boatBlue':(92,628,398,764),'boatPurple':(92,628,762,1130),'dock':(26,680,1136,1510),
   'rockBig':(608,992,20,456),'rockMid':(608,992,456,752),'rockSmall':(740,924,748,954),'buoy':(644,982,954,1224),'fish':(670,996,1240,1494)}
for k,(y0,y1,x0,x1) in SEA.items():ITEMS[k]=('sea2',y0,y1,x0,x1)
THR={k:4.0 for k in SEA}
# 실제로 뚫린 틈이 있는 물건만 안쪽 흰 바탕을 뚫는다
HOLES=set('windmill fenceWhite sled kite beehive palmA palmB crab tulipRed tulipYellow tulipPurple lanternOrange lanternPink bucketBlue bucketGreen skiSign dock butterfly lampYellow lampBlue owlPost'.split())
SNOWMEN=set('penguin'.split())
def clean_mask(n,M,C):
    lum=C.mean(2);sat=C.max(2)-C.min(2);h,w=M.shape
    yy=np.repeat(np.arange(h)[:,None],w,1)
    ys=np.where(M.any(1))[0];top,bot=ys.min(),ys.max()
    edge=M&~ndimage.binary_erosion(M,iterations=2)
    def drop(cond):
        lab,_=ndimage.label(cond);hit=set(np.unique(lab[edge&cond]))-{0}
        return np.isin(lab,list(hit))
    KEEPLOW=('swimRing','sled','hayBale','fenceWhite','snowballs','dock','buoy','rockBig','rockMid','rockSmall','fish','boatOrange','boatBlue','boatPurple')
    if n not in WHITE and n not in SKY and n not in KEEPLOW:     # 바닥 회색 그림자 얼룩
        M=M&~drop(M&(sat<22)&(lum>190)&(yy>top+(bot-top)*.68))
    if n in SKY:                            # 해·달·별·갈매기 아래 번짐
        M=M&~drop(M&(lum>226)&(sat<(10 if n in('gull','shellWhite','moonFull') else 46))&(yy>top+(bot-top)*.62))
    # 바닥 그림자 날개: 몸통보다 옆으로 넓게 퍼진 연한 무채색은 그림자
    ys=np.where(M.any(1))[0];top,bot=ys.min(),ys.max();Hh=bot-top
    band=(yy>bot-Hh*.12)
    body=M&(yy>bot-Hh*.30)&(yy<=bot-Hh*.14)
    if body.any() and n not in ('dock','rockBig','rockMid','rockSmall','buoy','fish','boatOrange','boatBlue','boatPurple','snowballs','skiSign','swimRing','sled','hayBale','fenceWhite'):
        xs=np.where(body.any(0))[0];bx0,bx1=xs.min()-3,xs.max()+3
        xx=np.repeat(np.arange(w)[None,:],h,0)
        wing=M&band&((xx<bx0)|(xx>bx1))&(sat<18)&(lum>195)
        M=M&~wing
        # 몸통 바로 아래 납작한 그림자 판(갈매기 발밑 등)
        if n=='gull':      # 발(주황)만 남기고 발밑 받침 제거
            M=M&~((yy>bot-Hh*.16)&(sat<85)&(lum>196))
        if n=='moonFull':  # 위쪽 윤곽으로 원을 맞춰 원 밖(아래 받침) 제거
            ys2,xs2=np.where(M&(yy<top+Hh*.6));cx=(xs2.min()+xs2.max())/2;r=(xs2.max()-xs2.min())/2;cy=top+r
            xx2=np.repeat(np.arange(w)[None,:],h,0);M=M&(((xx2-cx)**2+(yy-cy)**2)<=(r+2)**2)
        if n in ('starBig','sun','cloudNight'):   # 진한 색 몸통만 (아래 받침 제거)
            core=ndimage.binary_fill_holes(ndimage.binary_closing(M&(sat>(60 if n=='cloudNight' else 110)),iterations=3))
            M=M&ndimage.binary_dilation(core,iterations=2)
    if n=='swimRing':  # 빨간 줄무늬를 이은 타원 밖(받침) 제거
        ys2,xs2=np.where(M&(sat>90));cy=(ys2.min()+ys2.max())/2;cx=(xs2.min()+xs2.max())/2
        ry=(ys2.max()-ys2.min())/2+4;rx=(xs2.max()-xs2.min())/2+4
        xx2=np.repeat(np.arange(w)[None,:],h,0);M=M&(((xx2-cx)/rx)**2+((yy-cy)/ry)**2<=1)
    if n in SNOWMEN:                        # 눈사람·펭귄·이글루 아래 푸르스름한 그림자
        M=M&~drop(M&(sat<26)&(lum>196)&(lum<246)&(yy>top+(bot-top)*.86))
    if n in HOLES:   # 안쪽 틈의 흰 바탕
        hole=M&(lum>(249 if n=='fenceWhite' else 246))&(sat<(6 if n=='fenceWhite' else 8))
        lab,k=ndimage.label(hole)
        if k:
            sz=ndimage.sum(hole,lab,range(1,k+1));M=M&~np.isin(lab,[i+1 for i,v in enumerate(sz) if v>=18])
    return M
def matte(n):
    s,y0,y1,x0,x1=ITEMS[n]
    M,C=maskof(s,y0,y1,x0,x1,THR.get(n,7.0),n)
    if n in ('snowmanRed','snowmanGreen','snowmanBlue','shellWhite','snowBush','gull','snowballs'):
        pass
    M=clean_mask(n,M,C)
    # 가장자리에 붙은 바탕색 픽셀 벗기기 (흰 테두리 줄 없애기)
    bgc=np.median(np.concatenate([C[0],C[-1],C[:,0],C[:,-1]]),axis=0)
    pure=(np.abs(C-bgc).max(2)<=4)
    for _ in range(8):
        e=M&~ndimage.binary_erosion(M);rm=e&pure
        if not rm.any():break
        M=M&~rm
    b=np.median(np.concatenate([C[0],C[-1],C[:,0],C[:,-1]]),axis=0)
    FG=ndimage.binary_erosion(M,iterations=3); BG=~ndimage.binary_dilation(M,iterations=3); U=~FG&~BG
    # 가까운 확실한 안쪽 색 (7x7 평균)
    w=FG.astype(np.float32);k=(7,7)
    Fm=np.dstack([cv2.boxFilter(C[...,c].astype(np.float32)*w,-1,k,normalize=False) for c in range(3)])
    wn=cv2.boxFilter(w,-1,k,normalize=False)
    _,(iy,ix)=ndimage.distance_transform_edt(~FG,return_indices=True)
    Fn=np.where(wn[...,None]>0.5,Fm/np.maximum(wn,1e-6)[...,None],C[iy,ix])
    d=Fn-b;den=(d*d).sum(2);num=((C-b)*d).sum(2)
    a_un=np.clip(num/np.maximum(den,1e-6),0,1)
    # 흰 물건처럼 바탕과 색이 비슷한 곳은 거리 기반 부드러운 경계로
    dist_in=ndimage.distance_transform_edt(M);dist_out=ndimage.distance_transform_edt(~M)
    a_soft=np.clip(.5+(dist_in-dist_out)/1.6,0,1)
    rel=np.clip((np.sqrt(den)-25)/45,0,1)
    a=np.where(FG,1.0,np.where(BG,0.0,rel*a_un+(1-rel)*a_soft))
    # 경계 다듬기 (원래 그림을 길잡이로)
    guide=(C/255).astype(np.float32)
    a=cv2.ximgproc.guidedFilter(guide,a.astype(np.float32),2,1e-4)
    a=np.clip(a,0,1);a[FG]=1;a[BG]=0
    a[a<0.03]=0;a[a>0.97]=1
    # 색 되살리기: 흰 바탕을 빼서 원래 색
    au=np.maximum(a,1e-3)[...,None]
    Fun=np.clip(b+(C-b)/au,0,255)
    wgt=np.clip((a-.15)/.5,0,1)[...,None]
    F=np.where(U[...,None],wgt*Fun+(1-wgt)*Fn,C)
    out=np.dstack([F,a*255]).clip(0,255).astype(np.uint8)
    im=Image.fromarray(out,'RGBA');bb=im.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox()
    return im.crop(bb)
if __name__=='__main__':
    os.makedirs('cut11',exist_ok=True)
    names=sys.argv[1].split(',') if len(sys.argv)>1 else list(ITEMS)
    for n in names: matte(n).save(f'cut11/{n}.png')
    print(len(names))
