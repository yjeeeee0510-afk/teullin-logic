"""안드로이드 앱 아이콘·시작 화면 만들기 → app/android/app/src/main/res/

원본(있으면 사용, 없으면 icons/icon-512.png):
  art-src/app/icon.png         정사각 앱 아이콘(1024×1024 권장, 꽉 찬 그림)
  art-src/app/icon_fg.png      적응형 아이콘 앞 그림(투명 바탕, 1024×1024, 가운데 66% 안에 중요한 그림)
  art-src/app/icon_bg.png      적응형 아이콘 뒤 그림(1024×1024) — 없으면 icon.png 테두리 색
  art-src/app/splash.png       시작 화면 그림(세로 1080×1920 권장, 가운데에 로고) — 없으면 바탕색+아이콘
사용: python3 tools/app/make_res.py
"""
import os
from PIL import Image, ImageDraw
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES=os.path.join(ROOT,'app','android','app','src','main','res')
A=lambda n:os.path.join(ROOT,'art-src','app',n)
def load(n):
    p=A(n);return Image.open(p).convert('RGBA') if os.path.exists(p) else None
icon=load('icon.png') or Image.open(os.path.join(ROOT,'icons','icon-512.png')).convert('RGBA')
fg=load('icon_fg.png'); bgimg=load('icon_bg.png'); splash=load('splash.png')
edge=icon.resize((64,64)).getpixel((2,32))[:3]
D={'mdpi':1,'hdpi':1.5,'xhdpi':2,'xxhdpi':3,'xxxhdpi':4}
def save(im,folder,name):
    d=os.path.join(RES,folder);os.makedirs(d,exist_ok=True)
    if name.endswith('.webp'):
        old=os.path.join(d,name[:-5]+'.png')
        if os.path.exists(old): os.remove(old)
        im.save(os.path.join(d,name),quality=82,method=6)
    else: im.save(os.path.join(d,name))
for k,s in D.items():
    n=round(48*s); sq=icon.resize((n,n),Image.LANCZOS); save(sq,f'mipmap-{k}','ic_launcher.png')
    m=Image.new('L',(n*4,n*4),0);ImageDraw.Draw(m).ellipse((0,0,n*4-1,n*4-1),fill=255);m=m.resize((n,n),Image.LANCZOS)
    r=Image.new('RGBA',(n,n));r.paste(sq,(0,0),m);save(r,f'mipmap-{k}','ic_launcher_round.png')
    f=round(108*s); can=Image.new('RGBA',(f,f),(0,0,0,0))
    if fg is not None: can=fg.resize((f,f),Image.LANCZOS)
    else:
        inner=round(f*0.80); can=Image.new('RGBA',(f,f),edge+(255,)); can.alpha_composite(icon.resize((inner,inner),Image.LANCZOS),((f-inner)//2,(f-inner)//2))
    save(can,f'mipmap-{k}','ic_launcher_foreground.png')
    if bgimg is not None: save(bgimg.resize((f,f),Image.LANCZOS),f'mipmap-{k}','ic_launcher_background.png')
bgcol='#%02X%02X%02X'%edge
open(os.path.join(RES,'values','ic_launcher_background.xml'),'w').write(f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{bgcol}</color>\n</resources>\n')
if bgimg is not None:
    for x in ['ic_launcher.xml','ic_launcher_round.xml']:
        open(os.path.join(RES,'mipmap-anydpi-v26',x),'w').write('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n    <background android:drawable="@mipmap/ic_launcher_background"/>\n    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n</adaptive-icon>\n')
SPL={'mdpi':(320,480),'hdpi':(480,800),'xhdpi':(720,1280),'xxhdpi':(960,1600),'xxxhdpi':(1280,1920)}
def splash_img(w,h):
    if splash is not None:
        s=splash; sc=max(w/s.width,h/s.height); t=s.resize((round(s.width*sc),round(s.height*sc)),Image.LANCZOS)
        x=(t.width-w)//2;y=(t.height-h)//2;return t.crop((x,y,x+w,y+h))
    im=Image.new('RGBA',(w,h),(238,242,247,255)); n=round(min(w,h)*.42); im.alpha_composite(icon.resize((n,n),Image.LANCZOS),((w-n)//2,(h-n)//2)); return im
for k,(w,h) in SPL.items():
    save(splash_img(w,h).convert('RGB'),f'drawable-port-{k}','splash.webp'); save(splash_img(h,w).convert('RGB'),f'drawable-land-{k}','splash.webp')
save(splash_img(480,800).convert('RGB'),'drawable','splash.webp')
print('아이콘·시작 화면 완료', '(원본:', 'art-src/app' if os.path.exists(A('icon.png')) else 'icons/icon-512.png', ')')
