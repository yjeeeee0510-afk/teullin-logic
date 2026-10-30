"""로직 문제집(LOGIC_BANK)의 그림 문제마다 칸 색을 뽑아 index.html의 /*LOGIC_COLORS*/ 블록에 넣는다.

문제집은 그대로 두고, 각 문제(그림 이름)와 같은 모양이 나오는 물건 그림·설정(thr, detail)을 찾아
그 그림을 같은 방법으로 n×n으로 줄였을 때 칸마다의 평균 색(투명한 부분 제외)을 적는다.
형식: {"크기:문제코드": "칠한 칸 순서(가로줄 순)대로 #rgb 3글자씩"}
도형·무늬 문제는 게임 안에서 정한 색을 쓴다(LOGIC_SHAPE_COL 등).
실행: python3 tools/logic/colors.py
"""
import json, os, re, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen  # noqa: E402

ROOT = gen.ROOT


def cell_colors(path, n, thr, detail):
    """gen.from_alpha 와 같은 자르기·늘리기로, 칸마다 (투명도 가중) 평균 색."""
    im = Image.open(path).convert('RGBA')
    A = np.asarray(im).astype(float)
    a = A[..., 3] / 255
    ys, xs = np.where(a > 0.3)
    A = A[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = A.shape[:2]
    if max(h, w) / min(h, w) > 1.6:
        s_ = max(h, w); t = int(min(h, w) * 1.25)
        P = np.zeros((s_ if h >= w else t, t if h >= w else s_, 4)); oy = (P.shape[0] - h) // 2; ox = (P.shape[1] - w) // 2
        P[oy:oy + h, ox:ox + w] = A; A = P
    al = A[..., 3] / 255
    def box(ch):
        return np.asarray(Image.fromarray(ch.astype(np.float32), 'F').resize((n, n), Image.BOX)).astype(float)
    wa = box(al)
    rgb = np.stack([box(A[..., k] * al) for k in range(3)], -1) / np.maximum(wa, 1e-6)[..., None]
    return rgb


def hex3(c):
    # 작은 칸에서도 또렷하게 채도를 조금 올림
    c = np.clip(c, 0, 255); m = c.mean()
    c = np.clip(m + (c - m) * 1.18, 0, 255)
    return ''.join('0123456789abcdef'[int(round(v / 17))] for v in c)


def main():
    p = os.path.join(ROOT, 'index.html'); s = open(p, encoding='utf-8').read()
    m = re.search(r'/\*LOGIC_BANK\*/const LOGIC_BANK=(\{.*?\});/\*/LOGIC_BANK\*/', s, re.S)
    bank = json.loads(m.group(1))
    by_label = {}
    for f, label in gen.sprite_pictures():
        by_label.setdefault(label, []).append(f)
    out = {}; miss = []
    for ns, items in bank.items():
        n = int(ns)
        for it in items.split(','):
            code, _, label = it.partition('|')
            if not label or label not in by_label: continue
            found = None
            for f in by_label[label]:
                for detail in (True, False):
                    for thr in (.5, .42, .58):
                        G = gen.from_alpha(f, n, thr, detail)
                        if G is not None and G.shape == (n, n) and gen.encode(G) == code:
                            found = (f, thr, detail, G); break
                    if found: break
                if found: break
            if not found: miss.append((n, label)); continue
            f, thr, detail, G = found
            rgb = cell_colors(f, n, thr, detail)
            out[f'{n}:{code}'] = ''.join(hex3(rgb[y, x]) for y in range(n) for x in range(n) if G[y, x])
    js = 'const LOGIC_COLORS=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';'
    A_, B_ = '/*LOGIC_COLORS*/', '/*/LOGIC_COLORS*/'
    if A_ in s:
        i = s.index(A_); j = s.index(B_) + len(B_); s = s[:i] + A_ + js + B_ + s[j:]
    else:
        k = s.index('/*/LOGIC_BANK*/') + len('/*/LOGIC_BANK*/')
        s = s[:k] + '\n' + A_ + js + B_ + s[k:]
    open(p, 'w', encoding='utf-8').write(s)
    print('colored', len(out), 'missing', len(miss), miss[:10], 'bytes', len(js))


if __name__ == '__main__':
    main()
