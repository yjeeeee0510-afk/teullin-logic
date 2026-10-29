"""과자 나라 그림 누끼 (파란 바탕 물건 모음, 흰 바탕 과자 칸, 그대로 쓰는 지도·배경).

사용법: python3 tools/matting/candy.py <원본 폴더> <출력 폴더>
  원본 폴더 안 파일 이름
    stamps.png(도장 3×2) cake.png(쿠키·케이크 3×2) choco.png(초콜릿 3×2) candy.png(사탕·젤리 3×2)
    pads.png(발판 4×2) heart.png(쿠키 하트 2×1) buttons.png(버튼 3×1)   — 파란 바탕(#0047FF 근처)
    tiles.png(과자 칸 5×2, 흰 바탕)
    floor.png(지도 바닥 세로) gate.png(마을 입구 가로) bg.png(게임 배경 세로)
파란 바탕: 모서리에서 바탕색을 재고, 바탕색과의 거리로 알파를 매긴 뒤 바탕색을 빼서 색을 되살린다(언믹싱).
  도넛 구멍처럼 안쪽에 갇힌 바탕도 지운다(바탕색에 아주 가깝고 넓은 덩어리만, 파란 스프링클은 남김).
조각은 칸(격자)마다 한 물건으로 묶는다(곰젤리 3개, 사탕 지팡이 2개 등).
"""
import os, sys, json
import numpy as np
from PIL import Image
from scipy import ndimage

def bg_color(I):
    h, w, _ = I.shape
    s = np.concatenate([I[:12, :12].reshape(-1, 3), I[:12, -12:].reshape(-1, 3), I[-12:, :12].reshape(-1, 3), I[-12:, -12:].reshape(-1, 3)])
    return np.median(s, 0)

def blue_matte(rgb, t0=38, soft=70, hole_area=60):
    I = rgb.astype(np.float32)
    bg = bg_color(I)
    d = np.sqrt(((I - bg) ** 2).sum(2))
    near = d < t0 + 20
    lab, n = ndimage.label(near)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    sizes = ndimage.sum(np.ones_like(d), lab, range(n + 1))
    holes = [i for i in range(1, n + 1) if sizes[i] >= hole_area and i not in edge and (d[lab == i] < t0).mean() > 0.8]
    bgm = np.isin(lab, list(edge) + holes)
    # 물건 사이에 갇힌 그늘진 파란 바탕(곰젤리 사이 등): 파랑이 아주 강하게 튀는 덩어리
    r_, g_, b_ = I[..., 0], I[..., 1], I[..., 2]
    mx = np.maximum(r_, g_)
    deep = (b_ - mx > 70) & (b_ > 2.0 * mx + 30)
    dl, dn = ndimage.label(deep)
    ds = ndimage.sum(np.ones_like(d), dl, range(dn + 1))
    bgm |= np.isin(dl, [i for i in range(1, dn + 1) if ds[i] >= 30])
    fg = ~bgm
    fg = ndimage.binary_opening(fg, iterations=1)
    inner = ndimage.binary_erosion(fg, iterations=3)
    outer = ndimage.binary_dilation(fg, iterations=2)
    a = np.clip((d - t0) / soft, 0, 1)
    A = np.where(inner, 1.0, np.where(outer, a, 0.0))
    A = ndimage.gaussian_filter(A, 0.6) * outer
    A[inner] = 1.0
    Am = A[..., None]
    C = np.where(Am > 0.03, (I - (1 - Am) * bg) / np.maximum(Am, 1e-3), I)
    C = np.clip(C, 0, 255)
    # 가장자리 파란 번짐 걷기: 반투명 띠에서 파랑이 빨강·초록보다 튀면 눌러 준다
    band = (A < 0.98) & (A > 0)
    r, g, b = C[..., 0], C[..., 1], C[..., 2]
    cap = np.maximum(r, g) + 25
    C[..., 2] = np.where(band & (b > cap), cap, b)
    # 틈에 남은 진한 파랑(그늘진 바탕): 원래 색 기준으로 파랑만 튀는 칸은 지운다
    mx0 = np.maximum(I[..., 0], I[..., 1])
    left = (I[..., 2] > 2 * mx0 + 15) & (I[..., 2] > 35)
    left = ndimage.binary_dilation(left, iterations=1)
    A = np.where(left, 0.0, A)
    return fg, C, A

def white_matte(rgb, thr=10, soft=40):
    I = rgb.astype(np.float32)
    d = (255 - I).max(2)
    near = d < thr
    lab, _ = ndimage.label(near)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bgm = np.isin(lab, list(edge))
    fg = ndimage.binary_fill_holes(~bgm)
    fg = ndimage.binary_opening(fg, iterations=1)
    inner = ndimage.binary_erosion(fg, iterations=3)
    outer = ndimage.binary_dilation(fg, iterations=2)
    a = np.clip((d - 3) / soft, 0, 1)
    A = np.where(inner, 1.0, np.where(outer, a, 0.0))
    A = ndimage.gaussian_filter(A, 0.6) * outer
    A[inner] = 1.0
    Am = A[..., None]
    C = np.where(Am > 0.03, (I - (1 - Am) * 255) / np.maximum(Am, 1e-3), I)
    return fg, np.clip(C, 0, 255), A

def by_cell(fg, cols, rows, min_area=600):
    """격자 칸마다 그 칸에 중심이 있는 조각을 모두 묶는다."""
    lab, n = ndimage.label(fg)
    h, w = fg.shape
    cells = [[] for _ in range(cols * rows)]
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None: continue
        m = lab[sl] == i
        area = m.sum()
        if area < min_area: continue
        ys, xs = np.nonzero(m)
        cy, cx = ys.mean() + sl[0].start, xs.mean() + sl[1].start
        c = min(cols - 1, int(cx / w * cols)); r = min(rows - 1, int(cy / h * rows))
        cells[r * cols + c].append(i)
    return lab, cells

def save(C, A, mask, path, height, pad=3):
    ys, xs = np.nonzero(mask)
    y0, y1 = max(0, ys.min() - pad), min(A.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(A.shape[1], xs.max() + pad + 1)
    rgba = np.dstack([C[y0:y1, x0:x1], (A * mask)[y0:y1, x0:x1] * 255]).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox()
    im = im.crop(bb)
    if height and im.height > height:
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    im.save(path, 'WEBP', quality=90, method=6)
    return im.size

SHEETS = {
    'stamps':  (3, 2, ['stampCookie', 'stampMacaron', 'stampDonut', 'stampCandy', 'stampJelly', 'stampCrown'], 200),
    'cake':    (3, 2, ['cdCookieHouse', 'cdCupcake', 'cdCake', 'cdDonut', 'cdCream', 'cdMacaronTower'], 260),
    'choco':   (3, 2, ['cdChocoCastle', 'cdChocoFountain', 'cdChocoBridge', 'cdTruffle', 'cdChocoTree', 'cdClockTower'], 260),
    'candy':   (3, 2, ['cdLollyTree', 'cdGummyBears', 'cdCandyFlower', 'cdJellyMush', 'cdCottonBush', 'cdCandyCane'], 260),
    'pads':    (4, 2, ['padMacPink', 'padMacMint', 'padMacYellow', 'padJelly', 'padBeanGreen', 'padBeanPurple', 'padMallow', 'padCookie'], 140),
    'heart':   (2, 1, ['cookieFull', 'cookieEmpty'], 160),
    'buttons': (3, 1, ['btnCandyHouse', 'btnCookieBoat', 'btnCandyShop'], 240),
}
TILE_NAMES = ['tileStrawberry', 'tileChoco', 'tileButter', 'tileMint', 'tileBlueberry',
              'tileGrape', 'tileOrange', 'tileMatcha', 'tileWafer', 'tileCherry']

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    rep = {}
    for key, (cols, rows, names, hgt) in SHEETS.items():
        rgb = np.array(Image.open(os.path.join(src, key + '.png')).convert('RGB'))
        fg, C, A = blue_matte(rgb)
        lab, cells = by_cell(fg, cols, rows)
        for n, ids in zip(names, cells):
            assert ids, (key, n)
            mask = ndimage.binary_dilation(np.isin(lab, ids), iterations=3)
            rep[n] = save(C, A, mask, os.path.join(dst, n + '.webp'), hgt)
    # 과자 칸: 흰 바탕 5×2, 정사각으로
    rgb = np.array(Image.open(os.path.join(src, 'tiles.png')).convert('RGB'))
    fg, C, A = white_matte(rgb)
    lab, cells = by_cell(fg, 5, 2, min_area=3000)
    # 칸 격자가 그림 가운데 띠에만 있으므로 행은 위치로 다시 나눈다
    lab, n = ndimage.label(fg)
    objs = [(sl, i) for i, sl in enumerate(ndimage.find_objects(lab), 1) if (lab[sl] == i).sum() > 8000]
    objs.sort(key=lambda o: (o[0][0].start + o[0][0].stop) / 2)
    top, bot = objs[:5], objs[5:]
    objs = sorted(top, key=lambda o: o[0][1].start) + sorted(bot, key=lambda o: o[0][1].start)
    assert len(objs) == 10, len(objs)
    for nme, (sl, i) in zip(TILE_NAMES, objs):
        mask = ndimage.binary_dilation(lab == i, iterations=2)
        ys, xs = np.nonzero(mask)
        rgba = np.dstack([C, A * mask * 255]).astype(np.uint8)
        im = Image.fromarray(rgba, 'RGBA').crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        side = max(im.size)
        sq = Image.new('RGBA', (side, side), (0, 0, 0, 0)); sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
        sq = sq.resize((128, 128), Image.LANCZOS)
        sq.save(os.path.join(dst, nme + '.webp'), 'WEBP', quality=90, method=6)
        rep[nme] = sq.size
    # 지도 바닥: 위·아래 끝을 섞어 세로로 이어 붙여도 이음새가 안 보이게
    fl = np.array(Image.open(os.path.join(src, 'floor.png')).convert('RGB')).astype(np.float32)
    H = fl.shape[0]; k = 160
    top = fl[:k].copy(); bot = fl[H - k:].copy()
    w = np.linspace(0, 1, k)[:, None, None]
    seam = bot * (1 - w) + top * w            # 아래 끝 → 위 끝으로 부드럽게
    out = np.concatenate([fl[k:H - k], seam])  # 위쪽 k줄은 아래로 옮겨 섞음
    Image.fromarray(out.astype(np.uint8)).resize((720, round(out.shape[0] * 720 / 1024)), Image.LANCZOS).save(os.path.join(dst, 'candyFloor.jpg'), quality=86)
    g = Image.open(os.path.join(src, 'gate.png')).convert('RGB')
    g.resize((900, 600), Image.LANCZOS).save(os.path.join(dst, 'candyGate.jpg'), quality=86)
    b = Image.open(os.path.join(src, 'bg.png')).convert('RGB')
    b.resize((720, 1080), Image.LANCZOS).save(os.path.join(dst, 'candyBg.jpg'), quality=84)
    print(json.dumps(rep, ensure_ascii=False))
