"""OpenAI로 만든 그림(out/raw)을 게임 크기에 맞춰 img/ 에 넣는다.

사용법: python3 tools/ai_art/process.py [이름,이름 ...]   (이름을 안 주면 out/raw 에 있는 것 전부)
필요: pip install pillow

- 배경(scene): 가운데를 4:3으로 잘라 800×600 으로 → img/scenes/<이름>.png
- 물건·하늘(sprite/sky): 투명한 가장자리를 잘라내고 높이 400px 으로 → img/sprites/<이름>.png
  바탕이 투명하지 않으면(흰 바탕 등) 네 모서리에서 이어진 바탕색을 지운다.
- 바꾸기 전 원래 그림은 out/backup/ 에 한 번만 보관한다. 되돌리려면 그 파일을 img/ 에 다시 복사.
- 끝나면 sw.js 의 CACHE 버전을 하나 올리고, 확인용 그림 out/preview.png 를 만든다.
"""
import json
import os
import re
import shutil
import sys
from collections import deque

from PIL import Image, ImageDraw

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(DIR))
RAW = os.path.join(DIR, 'out', 'raw')
BACKUP = os.path.join(DIR, 'out', 'backup')
SPRITE_H = 400

spec = json.load(open(os.path.join(DIR, 'items.json'), encoding='utf-8'))
types = {i['name']: i['type'] for i in spec['items']}
names = sys.argv[1].split(',') if len(sys.argv) > 1 else sorted(f[:-4] for f in os.listdir(RAW) if f.endswith('.png'))


def remove_flat_background(im):
    """바탕이 투명하지 않은 그림: 모서리에서 이어진 비슷한 색을 투명하게."""
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    bg = tuple(sorted(c[k] for c in corners)[2] for k in range(3))
    close = lambda c: sum(abs(c[k] - bg[k]) for k in range(3)) < 48
    seen = bytearray(w * h)
    q = deque((x, y) for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y * w + x]:
            continue
        seen[y * w + x] = 1
        c = px[x, y]
        if c[3] == 0 or close(c):
            px[x, y] = (c[0], c[1], c[2], 0)
            q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return im


def sprite(src, dst):
    im = Image.open(src).convert('RGBA')
    if im.getchannel('A').getextrema()[0] == 255:  # 투명한 곳이 하나도 없음
        im = remove_flat_background(im)
    box = im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
    if not box:
        raise ValueError('그림이 비어 있어요')
    im = im.crop(box)
    s = SPRITE_H / im.height
    im = im.resize((max(1, round(im.width * s)), SPRITE_H), Image.LANCZOS)
    im.save(dst, optimize=True)


def scene(src, dst):
    im = Image.open(src).convert('RGB')
    w, h = im.size
    tw = min(w, round(h * 4 / 3))
    th = round(tw * 3 / 4)
    im = im.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th)).resize((800, 600), Image.LANCZOS)
    im.save(dst, optimize=True)


os.makedirs(BACKUP, exist_ok=True)
done = []
for n in names:
    src = os.path.join(RAW, f'{n}.png')
    if n not in types or not os.path.exists(src):
        print(f'{n}: 건너뜀 (목록에 없거나 그림이 없음)')
        continue
    sub = 'scenes' if types[n] == 'scene' else 'sprites'
    dst = os.path.join(ROOT, 'img', sub, f'{n}.png')
    if os.path.exists(dst) and not os.path.exists(os.path.join(BACKUP, f'{sub}-{n}.png')):
        shutil.copy(dst, os.path.join(BACKUP, f'{sub}-{n}.png'))
    try:
        (scene if sub == 'scenes' else sprite)(src, dst)
        done.append((n, dst))
        print(f'{n}: 완료 → img/{sub}/{n}.png')
    except Exception as e:
        print(f'{n}: 실패 ({e})')

if done:
    sw = os.path.join(ROOT, 'sw.js')
    s = open(sw, encoding='utf-8').read()
    s = re.sub(r"const CACHE='sekan-v(\d+)';", lambda m: f"const CACHE='sekan-v{int(m.group(1)) + 1}';", s, count=1)
    open(sw, 'w', encoding='utf-8').write(s)
    cell, cols = 170, 8
    rows = (len(done) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * cell, rows * (cell + 16)), '#9fb4cc')
    d = ImageDraw.Draw(sheet)
    for k, (n, f) in enumerate(done):
        im = Image.open(f).convert('RGBA')
        im.thumbnail((cell - 10, cell - 10))
        x, y = (k % cols) * cell, (k // cols) * (cell + 16)
        sheet.paste(im, (x + 5, y + 5), im)
        d.text((x + 4, y + cell), n, fill='black')
    sheet.save(os.path.join(DIR, 'out', 'preview.png'))
    print(f'\n{len(done)}장 넣음. sw.js 캐시 버전을 올렸어요. 확인용 그림: tools/ai_art/out/preview.png')
