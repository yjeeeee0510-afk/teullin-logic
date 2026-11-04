"""천국(6지역)·지역별 선착장 그림 넣기 (2026-11-04).

먼저: python3 tools/matting/chroma.py H1 H2 H3 H4 H5 H6 I3:I3_02 B1 D1 D2 D3 D4 D5 D6
- 물건 → img/sprites/<이름>.webp, 이동 장면용(islHeaven·pegBody·pegWing·carriage·pegCarriage) → img/voyage/
- 배경 BG25~29 (art-src/heaven): 틀린그림 배경·인게임 배경·지도 바닥(위아래 이음)·지도 끝·천마 이동 하늘(좌우 이음)
"""
import os, glob, shutil
import numpy as np
from PIL import Image
from apply_new import cover, seamless_v

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'tools', 'matting', 'out')
SRC = os.path.join(ROOT, 'art-src', 'heaven')
P = lambda *a: os.path.join(ROOT, *a)
VOY = {'islHeaven', 'pegBody', 'pegWing', 'carriage', 'pegCarriage'}
SKIP = {'heavenDock'}


def seamless_h(im, band=200):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    W = a.shape[1]
    t = np.linspace(0, 1, band)[None, :, None]; t = t * t * (3 - 2 * t)
    mix = a[:, W - band:] * (1 - t) + a[:, :band] * t
    out = np.concatenate([mix, a[:, band:W - band]], 1)
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def main():
    names = []
    for f in sorted(glob.glob(os.path.join(OUT, '*.webp'))):
        n = os.path.basename(f)[:-5]
        if n in SKIP: continue
        d = 'img/voyage' if n in VOY else 'img/sprites'
        shutil.copy(f, P(d, n + '.webp')); names.append(n)
    S = lambda k: Image.open(os.path.join(SRC, f'BG{k}.png')).convert('RGB')
    cover(S(25), 800, 600, 0.5).save(P('img/scenes', 'heaven.jpg'), quality=90)
    cover(S(26), 600, 900, 0.5).save(P('img/bg', 'zone5-heaven.jpg'), quality=86)
    seamless_v(S(27).resize((720, 1080), Image.LANCZOS), band=150).save(P('img/map', 'zone5.jpg'), quality=86)
    cover(S(28), 1152, 768, 0.5).save(P('img/map', 'shore5.jpg'), quality=86)
    seamless_h(cover(S(29), 2304 + 200, 768, 0.5), 200).save(P('img/voyage', 'heavenSky.jpg'), quality=86)
    print(len(names), ' '.join(names))


if __name__ == '__main__':
    main()
