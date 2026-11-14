"""6.7 지팀장 꾸미기·이동 그림(art-src/cos/*.png) → 게임 그림(img/…) + 머리 위치 표(ANCH).
사용: python3 tools/matting/build_cos.py [장 이름들]  (없으면 전부, 4코어 병렬)
- 누끼: chroma.matte. 흰 바탕 T1은 바깥 윤곽만 따고 안쪽을 채움(안쪽 흰 광택이 구멍이 되지 않게).
- 결과: img/voyage, img/acc, img/ped, img/badge, img/pair, img/candy(tileLemon·tileSoda), img/cosbg
- 동행 쌍마다 왼쪽·오른쪽 머리 위치를 재서 tools/matting/out/anch.json 에 적음(소품 얹기용)."""
import os, sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chroma
ROOT = chroma.ROOT
REQ = json.load(open(os.path.join(ROOT, 'art-src', 'request-cosmetics.json'), encoding='utf-8'))
SH = {s['id']: s for s in REQ['sheets']}
SRC = os.path.join(ROOT, 'art-src', 'cos')
OUT = os.path.join(ROOT, 'tools', 'matting', 'out')

def dest(nm):
    if nm.startswith('vyBoat') or nm in ('waveBandA', 'waveBandB', 'bowSplash', 'wakeTrail', 'dropsA', 'dropsB'):
        return 'img/voyage', {'vyBoatOrange': 300, 'vyBoatBlue': 300, 'vyBoatPurple': 300, 'waveBandA': 150, 'waveBandB': 150, 'bowSplash': 220, 'wakeTrail': 100, 'dropsA': 130, 'dropsB': 130}[nm]
    if nm.startswith('acc'): return None, 0   # 소품은 6.7에서 뺌(캐릭터와 겹쳐 어색)
    if nm.startswith('ped'): return 'img/ped', 220
    if nm.startswith('badge_'): return 'img/badge', 192
    if nm.startswith('tile'): return 'img/candy', 128
    if nm.startswith('pair'): return 'img/pair', 500
    return None, 0

def crop(im, pad=3):
    bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(bb)
    c = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0)); c.paste(im, (pad, pad)); return c

def head(a, x0, x1):
    """알파 a[:, x0:x1]에서 머리 위치: (가운데 x, 맨 위 y, 머리 너비) 픽셀"""
    sub = a[:, x0:x1] > 40
    rows = np.where(sub.any(1))[0]
    if not len(rows): return None
    top, bot = rows[0], rows[-1]; H = bot - top + 1
    r = min(sub.shape[0] - 1, top + int(H * .22))
    cols = np.where(sub[r])[0]
    xs = np.where(sub[top:top + int(H * .3)].any(0))[0]
    cx = (cols.min() + cols.max()) / 2 + x0 if len(cols) else (xs.min() + xs.max()) / 2 + x0
    return cx, top, (cols.max() - cols.min() + 1) if len(cols) else (xs.max() - xs.min() + 1)

def anchors(im):
    a = np.asarray(im.getchannel('A')); W, H = im.size
    mid = np.where(a[:, int(W * .3):int(W * .7)].astype(float).sum(0) == a[:, int(W * .3):int(W * .7)].astype(float).sum(0).min())[0]
    m = int(W * .3) + int(np.median(mid)) if len(mid) else W // 2
    L, R = head(a, 0, m), head(a, m, W)
    f = lambda h: [round(h[0] / W * 100, 1), round(h[1] / H * 100, 1), round(h[2] / W * 100, 1)]
    return [round(W / H, 3)] + f(L) + f(R)

def work(sh):
    m = SH[sh]; names = [i['id'] for i in m['items']]
    rgb = np.asarray(Image.open(os.path.join(SRC, sh + '.png')).convert('RGB'))
    rgba, K = chroma.matte(rgb)
    rgba = np.asarray(rgba).copy() if not isinstance(rgba, np.ndarray) else rgba.copy()
    res = {}
    if sh == 'T1':
        a = rgba[..., 3]; filled = ndimage.binary_fill_holes(a > 128)
        fix = ndimage.binary_erosion(filled, iterations=3) & (a < 255)
        rgba[fix, :3] = rgb[fix]; rgba[fix, 3] = 255
    parts = chroma.split_cells(rgba, len(names), m.get('cols', 3)) if sh != 'T1' else None
    if sh == 'T1':
        im = Image.fromarray(rgba.astype(np.uint8), 'RGBA'); w = im.width // 2
        parts = [im.crop((0, 0, w, im.height)), im.crop((w, 0, im.width, im.height))]
    for nm, im in zip(names, parts):
        d, h = dest(nm)
        if im is None or d is None: continue
        im = crop(im if isinstance(im, Image.Image) else Image.fromarray(im))
        if nm.startswith('pair'): res[nm] = anchors(im)
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
        im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS).save(os.path.join(ROOT, d, nm + '.webp'), 'WEBP', quality=90, method=6)
    return res

def v2c():
    for f, nm in (('V2C_A', 'waveBandA'), ('V2C_B', 'waveBandB'), ('V2C_C', 'bowSplash'), ('V2C_D', 'wakeTrail')):
        rgb = np.asarray(Image.open(os.path.join(SRC, f + '.png')).convert('RGB'))
        rgba, K = chroma.matte(rgb); im = crop(Image.fromarray(np.asarray(rgba).astype(np.uint8), 'RGBA'))
        d, h = dest(nm)
        im.resize((round(im.width * h / im.height), h), Image.LANCZOS).save(os.path.join(ROOT, d, nm + '.webp'), 'WEBP', quality=90, method=6)

def bgs():
    ids = {1: 'candy', 2: 'flower', 3: 'sea', 4: 'snow', 5: 'night', 6: 'dots', 7: 'sunset', 8: 'aurora', 9: 'gold'}
    os.makedirs(os.path.join(ROOT, 'img/cosbg'), exist_ok=True)
    for i, k in ids.items():
        Image.open(os.path.join(SRC, 'CB0%d.png' % i)).convert('RGB').resize((512, 768), Image.LANCZOS).save(os.path.join(ROOT, 'img/cosbg/bg_%s.webp' % k), 'WEBP', quality=82, method=6)

def solo():
    out = {}
    for i in range(12):
        im = Image.open(os.path.join(ROOT, 'img/zbody/b%d.webp' % i)).convert('RGBA'); a = np.asarray(im.getchannel('A')); W, H = im.size
        h = head(a, 0, W)
        out[i] = [round(W / H, 3), round(h[0] / W * 100, 1), round(h[1] / H * 100, 1), round(h[2] / W * 100, 1)]
    return out

if __name__ == '__main__':
    sheets = sys.argv[1:] or ['V1', 'V2', 'C1', 'C2', 'B1', 'B2', 'BD1', 'BD2', 'T1'] + ['P%02d' % i for i in range(1, 18)]
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p: rs = p.map(work, sheets)
    pairs = {}
    for r in rs: pairs.update({k[4:]: v for k, v in r.items()})
    v2c(); bgs()
    json.dump({'solo': solo(), 'pair': pairs}, open(os.path.join(OUT, 'anch.json'), 'w'))
    print('끝', len(pairs), '쌍')
