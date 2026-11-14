"""6.7 소품(모자 등)을 얹을 머리 위치 표. 혼자 서 있는 12마리는 눈으로 잰 값(SOLO), 동행 쌍은 쌍 그림에서
각 친구의 몸 범위를 재서 혼자 그림의 비율로 환산. 결과 JSON을 index.html의 /*ANCH*/ 에 넣는다.
SOLO = [가운데 x%, 머리 윗부분 y%, 머리 너비%]  (zbody 그림 기준)"""
import os, sys, json
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOLO = {0: (48, 9, 62), 1: (58, 7, 56), 2: (50, 5, 68), 3: (52, 22, 60), 4: (52, 12, 50), 5: (70, 4, 48),
        6: (52, 7, 55), 7: (60, 4, 60), 8: (53, 7, 60), 9: (42, 5, 30), 10: (50, 4, 62), 11: (55, 10, 62)}

def solo():
    out = {}
    for i, (x, y, w) in SOLO.items():
        im = Image.open(os.path.join(ROOT, 'img/zbody/b%d.webp' % i)); out[i] = [round(im.width / im.height, 3), x, y, w]
    return out

def half(a, x0, x1):
    s = a[:, x0:x1] > 40; r = np.where(s.any(1))[0]; c = np.where(s.any(0))[0]
    return c.min() + x0, c.max() + x0, r.min(), r.max()

def pair(a_i, b_i, path, S):
    im = Image.open(path); W, H = im.size; a = np.asarray(im.getchannel('A'))
    sums = (a[:, int(W * .35):int(W * .65)] > 40).sum(0); m = int(W * .35) + int(np.argmin(sums))
    res = [round(W / H, 3)]
    for (x0, x1), k in (((0, m), a_i), ((m, W), b_i)):
        l, r, t, b = half(a, x0, x1); _, cx, ty, hw = S[k]
        chH = b - t + 1
        res += [round((l + cx / 100 * (r - l)) / W * 100, 1), round((t + ty / 100 * chH) / H * 100, 1), round(hw / 100 * S[k][0] * chH / W * 100, 1)]
    return res

if __name__ == '__main__':
    S = solo(); out = {'solo': S, 'pair': {}}
    for i in range(12):
        for j in range(i + 1, 12):
            p = os.path.join(ROOT, 'img/pair/pair%d_%d.webp' % (i, j))
            if os.path.exists(p): out['pair']['%d_%d' % (i, j)] = pair(i, j, p, S)
    json.dump(out, open(os.path.join(ROOT, 'tools/matting/out/anch2.json'), 'w'), separators=(',', ':'))
    print(len(out['pair']))
