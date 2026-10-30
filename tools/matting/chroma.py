"""단색 바탕(초록 #00B140·파랑 #0047FF·마젠타 #FF00FF) 물건 모음 → 물건별 투명 WebP. 포토샵 수준 누끼 기준(CLAUDE.md)용.

사용법: python3 tools/matting/chroma.py F1 F2 ...   (art-src/new/<장>.png, 칸 순서는 art-src/request.json)
결과: tools/matting/out/<이름>.webp (게임 그림과 같은 높이) + tools/matting/out/qa_<장>.png 검수표

처리
1. 바탕색 K = 테두리 중앙값(장마다 실제 색을 잼). 픽셀마다 K와의 색 거리 d.
2. 확실한 안쪽(d 큼, 가장자리에서 3px 안쪽) / 확실한 바탕(d 작음, 바깥과 이어짐) / 그 사이 경계.
3. 경계 알파 = 가장 가까운 안쪽 색 F와 K 사이에서 이 픽셀이 어디쯤인지(언믹싱, 투영).
4. 색 정화: 경계 픽셀 색 = (C − (1−α)K)/α 를 안쪽 색 쪽으로 살짝 당김 → 바탕색 테두리 없음.
5. 바탕색 번짐 제거(despill): 초록 바탕이면 G를 max(R,B)+여유 이하로, 파랑이면 B, 마젠타면 R·B를 줄임(경계 근처만).
6. 물건 안 구멍: 바탕과 이어진 진짜 틈(튜브 가운데 등)은 투명, 안쪽 색이 바탕과 비슷해도 둘러싸인 곳은 불투명.
7. 칸 나누기: 덩어리 무게중심이 들어 있는 칸(줄×3칸)으로 물건을 모음 → 벌·더듬이 같은 떨어진 조각도 같은 물건.
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'tools', 'matting', 'out')


def key_color(rgb):
    b = np.concatenate([rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3), rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)])
    return np.median(b, 0)


def despill(C, K, w):
    """경계 근처(w=1)에서 바탕색 성분 줄이기."""
    C = C.copy()
    r, g, b = C[..., 0], C[..., 1], C[..., 2]
    if K[1] > K[0] and K[1] > K[2]:          # 초록 바탕
        lim = np.maximum(r, b) + 12
        C[..., 1] = np.where(g > lim, g - (g - lim) * w, g)
    elif K[2] > K[0] and K[2] > K[1]:        # 파랑 바탕
        lim = np.maximum(r, g) + 18
        C[..., 2] = np.where(b > lim, b - (b - lim) * w, b)
    else:                                     # 마젠타 바탕
        m = np.minimum(r, b); lim = g + 18
        over = np.clip(m - lim, 0, None) * w
        C[..., 0] = r - over; C[..., 2] = b - over
    return C


def matte(rgb):
    C = rgb.astype(np.float32)
    K = key_color(C)
    d = np.sqrt(((C - K) ** 2).sum(2))
    # 바탕: 바깥과 이어진 '바탕에 아주 가까운' 곳
    near = d < 34
    lab, _ = ndimage.label(near)
    edge_ids = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge_ids))
    # 둘러싸인 작은 바탕색 구멍도 바탕으로 (튜브 가운데처럼 크게 뚫린 곳) — 넓이 400px 이상만
    lab2, n2 = ndimage.label(near & ~bg)
    if n2:
        sz = ndimage.sum(np.ones_like(d), lab2, range(1, n2 + 1))
        bg |= np.isin(lab2, [i + 1 for i, v in enumerate(sz) if v >= 400])
    obj = ~bg
    obj = ndimage.binary_opening(obj, iterations=1)
    inner = ndimage.binary_erosion(obj, iterations=3) & (d > 70)
    band = obj & ~inner | (ndimage.binary_dilation(obj, iterations=2) & ~obj & ~(d < 12))
    # 가장 가까운 안쪽 색 F (5x5 평균)
    _, (iy, ix) = ndimage.distance_transform_edt(~inner, return_indices=True)
    F = C[iy, ix]
    FK = F - K
    den = (FK * FK).sum(2)
    a_un = np.clip(((C - K) * FK).sum(2) / np.maximum(den, 1e-3), 0, 1)
    # 안쪽 색이 바탕과 비슷한 경우(초록 바탕 위 초록 잎)는 거리 기반으로
    a_d = np.clip((d - 20) / 70, 0, 1)
    rel = np.clip((np.sqrt(den) - 50) / 60, 0, 1)
    a = np.where(inner, 1.0, np.where(band, rel * a_un + (1 - rel) * a_d, np.where(obj, 1.0, 0.0)))
    a[bg & ~band] = 0
    a = ndimage.gaussian_filter(a, 0.5)
    a[inner] = 1
    a[a < 0.04] = 0
    # 색 정화
    A = np.maximum(a, 1e-3)[..., None]
    Fun = np.clip((C - (1 - A) * K) / A, 0, 255)
    w = np.clip((a - 0.15) / 0.6, 0, 1)[..., None]
    col = np.where((a < 1)[..., None], w * Fun + (1 - w) * F, C)
    near_edge = ndimage.binary_dilation(~inner, iterations=3).astype(np.float32)
    col = despill(col, K, near_edge * 0.9)
    return np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8), K


def split_cells(rgba, n):
    """물건 n개를 줄(3개씩, 마지막 줄은 나머지)로 나눠 읽는 순서대로. 줄은 세로 빈 띠로, 줄 안에서는 가로 빈 틈으로 나누고,
    작은 조각(벌·더듬이·반짝이)은 가장 가까운 큰 덩어리에 붙임. 한 줄짜리 넓은 그림(2172×724)도 같은 방법."""
    a = rgba[..., 3] > 20
    H, W = a.shape
    rows = (n + 2) // 3
    per = [3] * (rows - 1) + [n - 3 * (rows - 1)]
    # 줄 나누기: 가로 투영의 빈 띠 중 가장 넓은 rows-1 곳
    pr = a.sum(1)
    if rows == 1:
        bands = [(0, H)]
    else:
        gaps = []; run = None
        for y in range(H):
            if pr[y] == 0:
                run = y if run is None else run
            elif run is not None:
                gaps.append((y - run, run, y)); run = None
        inner = [g for g in gaps if g[1] > 0 and g[2] < H]
        cuts = sorted([(g[1] + g[2]) // 2 for g in sorted(inner, reverse=True)[:rows - 1]])
        if len(cuts) < rows - 1: cuts = [round(H * (i + 1) / rows) for i in range(rows - 1)]
        ys = [0] + cuts + [H]; bands = list(zip(ys[:-1], ys[1:]))
    out = []
    lab, k = ndimage.label(ndimage.binary_dilation(a, iterations=2))
    for (y0, y1), cnt in zip(bands, per):
        L = lab[y0:y1]; A = a[y0:y1]
        ids = [i for i in np.unique(L[A]) if i]
        comps = []
        for i in ids:
            m = (L == i) & A
            ys_, xs_ = np.where(m)
            comps.append([xs_.min(), xs_.max() + 1, int(m.sum()), [i]])
        comps.sort(key=lambda c: -c[2])
        big = comps[:cnt]
        for c in comps[cnt:]:
            cx = (c[0] + c[1]) / 2
            t = min(big, key=lambda g: 0 if g[0] <= cx <= g[1] else min(abs(cx - g[0]), abs(cx - g[1])))
            t[0] = min(t[0], c[0]); t[1] = max(t[1], c[1]); t[3] += c[3]
        big.sort(key=lambda g: g[0])
        for g in big:
            m = np.isin(L, g[3]) & A
            ys_, xs_ = np.where(m)
            yy0, yy1, xx0, xx1 = ys_.min(), ys_.max() + 1, xs_.min(), xs_.max() + 1
            sub = rgba[y0 + yy0:y0 + yy1, xx0:xx1].copy()
            sub[..., 3] = np.where(m[yy0:yy1, xx0:xx1], sub[..., 3], 0)
            out.append(Image.fromarray(sub, 'RGBA'))
        out += [None] * (cnt - len(big))
    return out


def game_height(name):
    for d in ('img/sprites', 'img/voyage', 'img/candy'):
        p = os.path.join(ROOT, d, name + '.webp')
        if os.path.exists(p): return Image.open(p).height
    return 260


def qa_sheet(sheet, items, path):
    BGS = [(255, 43, 214), (28, 34, 54), (255, 255, 255), (63, 174, 74), (233, 201, 139)]
    C = 170
    sh = Image.new('RGB', (C * len(BGS), (C + 4) * len(items) + 30), (240, 240, 244))
    dr = ImageDraw.Draw(sh)
    try: f = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 14, index=1)
    except Exception: f = None
    dr.text((6, 6), f'{sheet} 검수표 — 바탕: 분홍 · 남색 · 흰색 · 초록 땅 · 모래', fill=(30, 30, 40), font=f)
    for i, (nm, im) in enumerate(items):
        y = 30 + i * (C + 4)
        for j, bgc in enumerate(BGS):
            cell = Image.new('RGB', (C, C), bgc)
            t = im.copy(); t.thumbnail((C - 16, C - 30))
            cell.paste(t, ((C - t.width) // 2, 22 + (C - 30 - t.height) // 2), t)
            sh.paste(cell, (j * C, y))
        dr.text((6, y + 2), nm, fill=(255, 255, 255), font=f)
    sh.save(path)


def run(sheets):
    req = json.load(open(os.path.join(ROOT, 'art-src', 'request.json'), encoding='utf-8'))
    plan = {s['id']: [i['id'] for i in s['items']] for s in req['sheets']}
    os.makedirs(OUT, exist_ok=True)
    rep = {}
    for sh in sheets:
        rgb = np.asarray(Image.open(os.path.join(ROOT, 'art-src', 'new', sh + '.png')).convert('RGB'))
        rgba, K = matte(rgb)
        names = plan[sh]
        parts = split_cells(rgba, len(names))
        done = []
        for nm, im in zip(names, parts):
            if im is None: rep[nm] = '없음'; continue
            bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox(); im = im.crop(bb)
            pad = 3; canvas = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0)); canvas.paste(im, (pad, pad)); im = canvas
            h = game_height(nm)
            im2 = im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
            im2.save(os.path.join(OUT, nm + '.webp'), 'WEBP', quality=92, method=6)
            done.append((nm, im)); rep[nm] = f'{im2.width}x{im2.height}'
        qa_sheet(sh, done, os.path.join(OUT, f'qa_{sh}.png'))
    return rep


if __name__ == '__main__':
    print(json.dumps(run(sys.argv[1:]), ensure_ascii=False))
