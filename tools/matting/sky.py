"""하늘섬 그림 누끼 (흰 바탕 물건 모음·하늘섬, 초록 바탕 구름, 투명 배).

사용법: python3 tools/matting/sky.py <모음 사진 폴더> <출력 폴더>
  폴더 안 파일 이름: items.png(흰 바탕 18개), clouds.png(초록 바탕 구름 6 + 발판 4), isl.png(흰 바탕 하늘섬), ship.png(투명 배 3개)
흰 바탕: 테두리에서 이어진 흰색을 바탕으로 잡고, 경계 몇 px만 '흰색과 얼마나 다른가'로 반투명을 매긴 뒤
흰색을 빼서 색을 되살린다(언믹싱). 초록 바탕: 초록 우세 정도로 알파, 가장자리 초록 번짐 제거.
"""
import os, sys, json
import numpy as np
from PIL import Image
from scipy import ndimage

def comps(fg, min_area):
    lab, n = ndimage.label(fg)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        area = (lab[sl] == i).sum()
        if area >= min_area: out.append((sl, i))
    return lab, out

def white_matte(rgb, thr=10, soft=46, band=4):
    I = rgb.astype(np.float32)
    d = (255 - I).max(2)                       # 흰색에서 가장 많이 벗어난 채널
    near = d < thr
    bg = np.zeros(near.shape, bool)
    lab, _ = ndimage.label(near)
    edge_ids = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge_ids))
    fg = ndimage.binary_fill_holes(~bg)
    fg = ndimage.binary_opening(fg, iterations=1)
    inner = ndimage.binary_erosion(fg, iterations=band)
    outer = ndimage.binary_dilation(fg, iterations=2)
    a = np.clip((d - 3) / soft, 0, 1)
    A = np.where(inner, 1.0, np.where(outer, a, 0.0))
    A = ndimage.gaussian_filter(A, 0.6) * outer
    A[inner] = 1.0
    C = np.where(A[..., None] > 0.02, (I - (1 - A[..., None]) * 255) / np.maximum(A[..., None], 1e-3), I)
    return fg, np.clip(C, 0, 255), A

def green_matte(rgb):
    I = rgb.astype(np.float32)
    r, g, b = I[..., 0], I[..., 1], I[..., 2]
    dom = g - np.maximum(r, b)
    A = 1 - np.clip((dom - 18) / 70, 0, 1)
    A = ndimage.gaussian_filter(A, 0.5)
    C = I.copy()
    m = np.maximum(r, b)
    C[..., 1] = np.minimum(g, m + 6)          # 초록 번짐 걷기
    fg = A > 0.5
    return fg, C, A

def save(C, A, sl, path, pad=4, height=None):
    y, x = sl
    y0, y1 = max(0, y.start - pad), min(A.shape[0], y.stop + pad)
    x0, x1 = max(0, x.start - pad), min(A.shape[1], x.stop + pad)
    rgba = np.dstack([C[y0:y1, x0:x1], A[y0:y1, x0:x1] * 255]).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox()
    im = im.crop(bb)
    if height and im.height > height:
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    im.save(path, 'WEBP', quality=92, method=6)
    return im.size

def grid_sort(items, rows):
    # 행 경계(y)로 나누고 행 안에서는 x 순서
    out = []
    for (r0, r1) in rows:
        row = [it for it in items if r0 <= (it[0][0].start + it[0][0].stop) / 2 < r1]
        out += sorted(row, key=lambda it: it[0][1].start)
    return out

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    rep = {}
    # 1) 물건 18개
    rgb = np.array(Image.open(os.path.join(src, 'items.png')).convert('RGB'))
    fg, C, A = white_matte(rgb)
    lab, cs = comps(fg, 1500)
    cs = [c for c in cs if (c[0][1].stop - c[0][1].start) < 900]   # 가로 구분선 제외
    # 같은 물건의 떨어진 조각(연 꼬리 등)은 가까운 큰 덩어리에 붙인다
    big = [c for c in cs if (lab[c[0]] == c[1]).sum() > 8000]
    names = ['balloonRed','balloonBlue','kiteYellow','kiteGreen','pinwheelPink','pinwheelBlue',
             'cloudHouse','bellTower','weatherVane','birdHouse','airship','wingMail',
             'rainbowBridge','cloudTree','skyWhale','featherGold','featherPurple','starJar']
    big = grid_sort(big, [(0, 380), (380, 705), (705, 1024)])
    assert len(big) == 18, len(big)
    for n, (sl, i) in zip(names, big):
        y, x = sl
        # 이 상자 안의 모든 전경(작은 조각 포함)
        Ai = A.copy()
        keep = np.zeros(fg.shape, bool)
        yy0, yy1, xx0, xx1 = y.start, y.stop, x.start, x.stop
        sub = lab[yy0:yy1, xx0:xx1]
        ids = set(np.unique(sub)) - {0}
        ids = [k for k in ids if k == i or (lab == k).sum() < 8000]
        keep = np.isin(lab, ids)
        keep = ndimage.binary_dilation(keep, iterations=3)
        Ai = Ai * keep
        rep[n] = save(C, Ai, sl, os.path.join(dst, n + '.webp'), height=260)
    # 2) 구름 6 + 발판 4
    rgb = np.array(Image.open(os.path.join(src, 'clouds.png')).convert('RGB'))
    fg, C, A = green_matte(rgb)
    lab, cs = comps(fg, 3000)
    cs = grid_sort(cs, [(0, 400), (400, 770), (770, 1024)])
    cn = ['skyCloudA','skyCloudB','skyCloudC','skyCloudD','skyCloudE','skyCloudF','pebCloudA','pebCloudB','pebCloudC','pebCloudD']
    assert len(cs) == 10, len(cs)
    for n, (sl, i) in zip(cn, cs):
        keep = ndimage.binary_dilation(lab == i, iterations=3)
        rep[n] = save(C, A * keep, sl, os.path.join(dst, n + '.webp'), height=260 if n.startswith('sky') else 120)
    # 3) 하늘섬
    rgb = np.array(Image.open(os.path.join(src, 'isl.png')).convert('RGB'))
    fg, C, A = white_matte(rgb, thr=6, soft=40)
    lab, cs = comps(fg, 20)
    keepids = [i for sl, i in cs]
    allsl = ndimage.find_objects(np.isin(lab, keepids).astype(int))[0]
    rep['islSky'] = save(C, A, allsl, os.path.join(dst, 'islSky.webp'), height=420)
    # 4) 배: 투명 PNG, 알파 그대로 (투명 자리의 쓰레기 색은 알파 0 이라 무시)
    im = np.array(Image.open(os.path.join(src, 'ship.png')).convert('RGBA')).astype(np.float32)
    A = im[..., 3] / 255
    A[A < 0.06] = 0
    lab, cs = comps(A > 0.5, 5000)
    cs = sorted(cs, key=lambda c: c[0][1].start)
    sn = ['vyWingShip', 'vyShip', 'vyWing']
    assert len(cs) == 3, len(cs)
    for n, (sl, i) in zip(sn, cs):
        keep = ndimage.binary_dilation(lab == i, iterations=4)
        rep[n] = save(im[..., :3], A * keep, sl, os.path.join(dst, n + '.webp'), height=360 if n != 'vyWing' else 240)
    print(json.dumps(rep, ensure_ascii=False))
