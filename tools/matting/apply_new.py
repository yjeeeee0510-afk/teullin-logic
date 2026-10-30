"""새 그림(art-src/new) → 게임 그림(img/) 넣기. 먼저 `python3 tools/matting/chroma.py <장들>` 로 tools/matting/out/ 에 누끼를 만든다.

- 물건: out/<이름>.webp → img/sprites|voyage|candy (지금 있는 자리 그대로), 화면 아이콘 ico* → img/ui/ (높이 96px)
- wingShip = vyWingShip, palmB 는 좌우 반전(palmA와 반대로 기울게)
- 배경 BG01~24: 지역 5곳 × (틀린그림 배경·인게임 배경·지도 바닥·바닷가) + 옆 바다 + 과자 나라 3장
  지도 바닥·과자 지도 바닥은 위아래 이음매를 섞어 이어지게(seamless) 만든다.
"""
import os, glob, shutil
import numpy as np
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'tools', 'matting', 'out')
NEW = os.path.join(ROOT, 'art-src', 'new')
P = lambda *a: os.path.join(ROOT, *a)


def place_sprites():
    done = []
    for f in sorted(glob.glob(os.path.join(OUT, '*.webp'))):
        n = os.path.basename(f)[:-5]
        if n.startswith('ico'):
            os.makedirs(P('img/ui'), exist_ok=True)
            im = Image.open(f); im = im.resize((round(im.width * 96 / im.height), 96), Image.LANCZOS)
            im.save(P('img/ui', n + '.webp'), 'WEBP', quality=92, method=6); done.append('ui/' + n); continue
        for d in ('img/sprites', 'img/voyage', 'img/candy'):
            if os.path.exists(P(d, n + '.webp')):
                im = Image.open(f)
                if n == 'palmB': im = ImageOps.mirror(im)
                im.save(P(d, n + '.webp'), 'WEBP', quality=92, method=6); done.append(d.split('/')[1] + '/' + n); break
        else:
            print('자리 없음', n)
    shutil.copy(P('img/voyage/vyWingShip.webp'), P('img/sprites/wingShip.webp'))
    return done


def cover(im, w, h, ay=0.5):
    """비율 맞춰 가운데(세로는 ay 위치)를 잘라 w×h"""
    sw, sh = im.size; s = max(w / sw, h / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = round((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))


def seamless_v(im, band=160):
    """위아래가 이어지는 타일: 아래 band 줄을 위쪽으로 서서히 섞고, 아래 band는 잘라냄."""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    H = a.shape[0]
    top = a[:band]; bot = a[H - band:]
    t = np.linspace(0, 1, band)[:, None, None]
    t = t * t * (3 - 2 * t)
    mix = bot * (1 - t) + top * t
    out = np.concatenate([mix, a[band:H - band]], 0)
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def place_backgrounds():
    zones = [('flowerhill', 'zone0-flowerhill'), ('beach', 'zone1-sea'), ('snowmount', 'zone2-snow'), ('nightsky', 'zone3-night'), ('skyisland', 'zone4-sky')]
    for z, (scene, gbg) in enumerate(zones):
        k = z * 4 + 1
        S = lambda i: Image.open(os.path.join(NEW, 'bg', f'BG{k + i:02d}.png')).convert('RGB')
        cover(S(0), 800, 600, 0.5).save(P('img/scenes', scene + '.jpg'), quality=90)
        cover(S(1), 600, 900, 0.5).save(P('img/bg', gbg + '.jpg'), quality=86)
        tile = seamless_v(S(2).resize((720, 1080), Image.LANCZOS), band=150)
        tile.save(P('img/map', f'zone{z}.jpg'), quality=86)
        cover(S(3), 1152, 768, 0.5).save(P('img/map', f'shore{z}.jpg'), quality=86)
    sea = Image.open(os.path.join(NEW, 'bg', 'BG21.png')).convert('RGB')
    cover(sea, 2304, 768, 0.5).save(P('img/voyage/sea.jpg'), quality=86)
    cover(Image.open(os.path.join(NEW, 'bg', 'BG22.png')).convert('RGB'), 720, 1080).save(P('img/candy/candyBg.jpg'), quality=86)
    seamless_v(Image.open(os.path.join(NEW, 'bg', 'BG23.png')).convert('RGB').resize((720, 1080), Image.LANCZOS), 150).save(P('img/candy/candyFloor.jpg'), quality=86)
    cover(Image.open(os.path.join(NEW, 'bg', 'BG24.png')).convert('RGB'), 900, 600).save(P('img/candy/candyGate.jpg'), quality=86)


if __name__ == '__main__':
    d = place_sprites(); print('물건', len(d))
    place_backgrounds(); print('배경 완료')
