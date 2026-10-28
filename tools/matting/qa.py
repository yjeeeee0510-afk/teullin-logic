"""검수: 물건마다 12가지 바탕(단색 8 + 지역 땅 4) 위에 올려 보기."""
import sys,os,glob
from PIL import Image,ImageDraw
SOLID=[('검정',(0,0,0)),('흰색',(255,255,255)),('빨강',(229,57,53)),('초록',(67,160,71)),('파랑',(30,136,229)),('노랑',(253,216,53)),('보라',(142,36,170)),('회색',(128,128,128))]
TEX=['/home/claude/teullin-logic/img/scenes/flowerhill.jpg','/home/claude/teullin-logic/img/scenes/beach.jpg','/home/claude/teullin-logic/img/scenes/snowmount.jpg','/home/claude/teullin-logic/img/scenes/nightsky.jpg']
def bgs(cell):
    out=[Image.new('RGB',(cell,cell),c) for _,c in SOLID]
    for t in TEX:
        im=Image.open(t).convert('RGB');w,h=im.size;out.append(im.crop((w//2-120,h-260,w//2+120,h-20)).resize((cell,cell)))
    return out
def sheet(src,names,out,cell=120,zoom=1):
    B=bgs(cell);o=Image.new('RGB',(len(B)*cell,len(names)*cell),'white')
    for r,n in enumerate(names):
        im=Image.open(f'{src}/{n}.png').convert('RGBA');im.thumbnail((cell-8,cell-8),Image.LANCZOS)
        for c,bg in enumerate(B):
            t=bg.copy();t.paste(im,((cell-im.width)//2,(cell-im.height)//2),im);o.paste(t,(c*cell,r*cell))
    o.save(out)
if __name__=='__main__':
    sheet(sys.argv[1],sys.argv[2].split(','),sys.argv[3],int(sys.argv[4]) if len(sys.argv)>4 else 120)
