import json,sys,os
import numpy as np
from PIL import Image,ImageFilter
from scipy import ndimage
# 상자: 이름 -> (시트, y0,y1,x0,x1)
B={}
def add(sheet,rows):
    for n,y0,y1,x0,x1 in rows: B[n]=(sheet,y0,y1,x0,x1)
add('sea',[('lighthouse',10,470,40,232),('beachHutBlue',95,428,240,0),('beachHutPink',95,428,0,0),('beachHutMint',95,428,0,1030),
 ('palmA',50,446,1010,0),('palmB',50,446,0,1530),
 ('umbrellaRed',458,714,6,284),('umbrellaBlue',458,716,288,566),('umbrellaYellow',458,716,563,842),('sandcastle',460,724,845,1127),('shellPink',500,690,1127,1323),('shellWhite',505,690,1324,1520),
 ('starfishOrange',758,956,8,206),('starfishPink',760,956,206,400),('crab',760,948,404,660),('bucketBlue',730,958,676,852),('bucketGreen',742,964,868,1040),('swimRing',762,965,1046,1300),('gull',742,962,1308,1514)])
add('flower',[('windmill',2,398,28,335),('cottageRed',22,304,370,688),('cottageBlue',22,304,710,1030),('cottagePurple',22,304,1050,1370),
 ('blossomPink',312,618,224,516),('blossomWhite',312,618,532,823),('blossomYellow',309,618,840,1124),('treeRound',305,620,1165,1477),
 ('flowersPink',604,758,26,266),('flowersYellow',614,758,264,480),('flowersBlue',610,758,480,713),('flowersWhite',610,758,716,945),('tulipRed',600,753,961,1128),('tulipYellow',602,753,1148,1313),('tulipPurple',600,753,1326,1495),
 ('mushroomRed',790,979,40,280),('fenceWhite',814,970,291,582),('beehive',740,985,583,805),('hayBale',790,995,806,1115),('butterfly',812,985,1144,1322),('kite',743,1018,1340,1484)])
add('sky',[('puffA',60,338,22,478),('puffB',60,338,505,993),('puffC',58,338,1024,1513),('sun',335,663,18,348),('moonFull',367,668,363,655),('moonCrescent',370,660,674,934),('starBig',374,654,955,1244),('starWish',378,666,1262,1512),
 ('planetRing',666,974,34,469),('planetSmall',700,957,576,829),('cloudNight',660,965,924,1488)])
add('night',[('castleLilac',5,455,12,411),('observatory',88,457,412,714),('lampYellow',157,453,717,827),('lampBlue',157,453,852,963),('treeNightPurple',114,458,970,0),('treeNightTeal',114,458,0,1532),
 ('glowMushBlue',479,687,18,266),('glowMushPink',484,687,268,510),('glowMushGreen',482,687,524,766),('gemPurple',462,694,783,1023),('gemBlue',464,694,1029,1268),('gemPink',464,695,1276,1520),
 ('lanternOrange',711,978,111,280),('lanternPink',708,981,345,516),('bushNight',705,981,596,1025),('owlPost',688,996,1173,1341)])
add('snow',[('cabinRed',16,304,22,356),('cabinBrown',17,304,365,702),('cabinGreen',17,304,709,1050),('igloo',45,306,1093,1492),
 ('pineSnowA',307,607,29,273),('pineSnowB',308,607,275,500),('pineSnowC',308,608,499,727),('snowmanRed',325,609,762,1012),('snowmanBlue',327,609,1015,1262),('snowmanGreen',325,609,1268,1512),
 ('penguin',607,822,26,256),('sled',613,825,255,610),('snowBush',600,803,629,0),('iceBlue',600,821,1112,0),('icePurple',600,821,0,1521),
 ('snowballs',838,1004,150,573),('skiSign',797,1008,659,892)])

def split_col(sheet,y0,y1,x0,x1):
    # 붙어 있는 두 물건 사이에서 물건이 가장 적은 세로줄
    a=np.asarray(Image.open(sheet+'.png').convert('RGB')).astype(int)[y0:y1,x0:x1]
    d=np.abs(a-254).max(axis=2)>30
    col=d.sum(axis=0);w=len(col)
    mid=slice(int(w*.3),int(w*.7))
    return x0+int(np.argmin(col[mid]))+int(w*.3)
# 0으로 둔 경계는 자동으로 찾기
def fix(names,sheet,x0,x1,parts):
    y0=min(B[n][1] for n in names);y1=max(B[n][2] for n in names)
    xs=[x0]
    if parts==3:
        c1=split_col(sheet,y0,y1,x0,x0+(x1-x0)*2//3-0)  # 첫 경계
        # 첫 경계: 앞쪽 2/3 구간에서 중간
        c1=split_col(sheet,y0,y1,x0,x0+(x1-x0)*2//3)
        c2=split_col(sheet,y0,y1,c1,x1)
        xs+= [c1,c2]
    else: xs.append(split_col(sheet,y0,y1,x0,x1))
    xs.append(x1)
    for i,n in enumerate(names):
        s,a,b,_,_=B[n];B[n]=(s,a,b,xs[i],xs[i+1])
fix(['beachHutBlue','beachHutPink','beachHutMint'],'sea',240,1030,3)
fix(['palmA','palmB'],'sea',1010,1530,2)
fix(['treeNightPurple','treeNightTeal'],'night',970,1532,2)
fix(['iceBlue','icePurple'],'snow',1112,1521,2)
B['snowBush']=('snow',600,803,629,split_col('snow',600,803,629,1095))

OPT={
 'snowballs':dict(thr=1.5,lum=246,sat=6,peel=0,close=10,hull=1),'shellWhite':dict(thr=3,lum=240,sat=10,peel=2,close=8),'snowBush':dict(thr=3,lum=242,sat=10,peel=0),
 'gull':dict(thr=3,lum=242,sat=10,peel=0),'igloo':dict(peel=0),'puffA':dict(peel=0),'puffB':dict(peel=0),'puffC':dict(peel=0),
 'snowmanRed':dict(peel=0,close=8),'snowmanBlue':dict(peel=0),'snowmanGreen':dict(peel=0,close=8),'moonFull':dict(peel=1),
 'starWish':dict(sat=60,lum=200,thr=12),'moonCrescent':dict(sat=60,lum=200,thr=12),'sun':dict(sat=40,lum=200,thr=10),
 'windmill':dict(clear=[(315,600,250,400)]),'blossomPink':dict(clear=[(300,398,200,262)]),
}
def cutout(sheet,y0,y1,x0,x1,grad_thr=7.0,name=None):
    o=OPT.get(name,{});grad_thr=o.get('thr',grad_thr)
    im=Image.open(sheet+'.png').convert('RGB').crop((x0,y0,x1,y1))
    a=np.asarray(im).astype(float)
    lum=a.mean(axis=2);sat=a.max(axis=2)-a.min(axis=2)
    g=np.hypot(ndimage.sobel(lum,0),ndimage.sobel(lum,1))/4
    g=ndimage.maximum_filter(g,3)
    bglike=(sat<o.get('sat',16))&(lum>o.get('lum',185))&(g<grad_thr)
    for (cy0,cy1,cx0,cx1) in o.get('clear',[]):
        bglike[max(0,cy0-y0):max(0,cy1-y0),max(0,cx0-x0):max(0,cx1-x0)]=True
    lab,_=ndimage.label(bglike)
    edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(edge))
    obj=~bg
    obj=ndimage.binary_opening(obj,iterations=1)
    # 가장 큰 덩어리와, 그 크기의 2% 이상인 덩어리만 (이웃 물건 조각 제거)
    lab2,k=ndimage.label(ndimage.binary_dilation(obj,iterations=4))
    if k>1:
        sizes=ndimage.sum(obj,lab2,range(1,k+1))
        keep=[i+1 for i,s in enumerate(sizes) if s>=sizes.max()*0.02]
        # 상자 가장자리에 걸친 작은 조각은 이웃 물건 → 버림
        h,w=obj.shape
        def touches(i):
            sl=ndimage.find_objects((lab2==i).astype(int))[0]
            return sl[0].start==0 or sl[1].start==0 or sl[0].stop==h or sl[1].stop==w
        big=int(np.argmax(sizes))+1
        keep=[i for i in keep if i==big or not (touches(i) and sizes[i-1]<sizes.max()*0.25)]
        obj=obj&np.isin(lab2,keep)
    if o.get('close'):
        obj=ndimage.binary_closing(obj,structure=np.ones((3,3)),iterations=o['close'])
    obj=ndimage.binary_fill_holes(obj)
    if o.get('hull'):
        from scipy.spatial import ConvexHull
        from PIL import ImageDraw as _D
        labh,kh=ndimage.label(obj);m=Image.new('L',obj.shape[::-1],0);dr=_D.Draw(m)
        for i in range(1,kh+1):
            pts=np.argwhere(labh==i)
            if len(pts)<20: continue
            hv=ConvexHull(pts[:,::-1]);dr.polygon([tuple(pts[j,::-1]) for j in hv.vertices],fill=255)
        obj=np.asarray(m)>0
    for (cy0,cy1,cx0,cx1) in o.get('clear',[]):
        obj[max(0,cy0-y0):max(0,cy1-y0),max(0,cx0-x0):max(0,cx1-x0)]=False
    # 가장자리에 남은 연한 회색(그림자·흰 테두리) 벗겨내기
    neutral_light=(sat<14)&(lum>205)
    for _ in range(o.get('peel',4)):
        edge=obj&~ndimage.binary_erosion(obj)
        rm=edge&neutral_light
        if not rm.any(): break
        obj=obj&~rm
    alpha=Image.fromarray((obj*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
    rgba=im.convert('RGBA');rgba.putalpha(alpha)
    bb=alpha.point(lambda v:255 if v>20 else 0).getbbox()
    return rgba.crop(bb)

if __name__=='__main__':
    out=sys.argv[1];os.makedirs(out,exist_ok=True)
    thr=float(sys.argv[2]) if len(sys.argv)>2 else 7.0
    for n,(s,y0,y1,x0,x1) in B.items():
        cutout(s,y0,y1,x0,x1,thr,n).save(f'{out}/{n}.png')
    print(len(B),'cut')
    json.dump({k:list(v) for k,v in B.items()},open(out+'/_boxes.json','w'))
