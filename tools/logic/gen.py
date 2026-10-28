"""네모네모 로직 문제집 만들기.

사용법: python3 tools/logic/gen.py   → index.html 안의 LOGIC_BANK 블록을 새로 씀

- 출처: 게임 물건 그림 축소 그림, 도형, 대칭/비대칭 무늬, 예전 PICS
- 모든 문제는 줄 단위 추론만으로 끝까지 풀림(= 답이 하나) 을 확인
- 회전·뒤집기로 같은 그림, 서로 너무 비슷한 그림은 제외
- 크기별로 출처를 섞고, 쉬운 문제부터 어려운 문제 순으로 대략 정렬
"""
import glob, json, math, os, random, re
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIZES = [5, 6, 7, 8, 10, 12]
POOL = 120            # 크기마다 문제 수 (라운드 수의 4~12배 → 다시 해도 새 문제)
rng = random.Random(20261028)

# ---------------- 풀이기 ----------------
def clue(line):
    out, run = [], 0
    for v in line:
        if v: run += 1
        elif run: out.append(run); run = 0
    if run: out.append(run)
    return out

def line_solve(cl, cur, n):
    """cur: -1 모름, 0 빈칸, 1 칠함. 가능한 배치들의 공통 칸을 돌려줌 (모순이면 None)."""
    can1 = [False] * n; can0 = [False] * n; ok = False
    k = len(cl)
    suffix = [0] * (k + 1)
    for i in range(k - 1, -1, -1):
        suffix[i] = suffix[i + 1] + cl[i] + (1 if i < k - 1 else 0)
    memo = {}
    def fits0(a, b):
        return all(cur[i] != 1 for i in range(a, b))
    def rec(i, pos):
        # i번째 덩어리를 pos 이후에 놓기 → 가능한 (칸별) 결과를 memo 로 모음
        key = (i, pos)
        if key in memo: return memo[key]
        res = None
        if i == k:
            if fits0(pos, n):
                res = ([False] * n, [i2 >= pos for i2 in range(n)])
            memo[key] = res; return res
        L = cl[i]
        acc1 = [False] * n; acc0 = [False] * n; any_ = False
        last = n - suffix[i]
        for s in range(pos, last + 1):
            if not fits0(pos, s): break
            if any(cur[j] == 0 for j in range(s, s + L)): continue
            e = s + L
            if e < n and cur[e] == 1: continue
            nxt = e + 1 if i < k - 1 else e
            if i < k - 1 and e >= n: continue
            sub = rec(i + 1, min(nxt, n))
            if sub is None: continue
            any_ = True
            for j in range(pos, s): acc0[j] = True
            for j in range(s, e): acc1[j] = True
            if i < k - 1 and e < n: acc0[e] = True
            for j in range(n):
                if sub[0][j]: acc1[j] = True
                if sub[1][j]: acc0[j] = True
        res = (acc1, acc0) if any_ else None
        memo[key] = res; return res
    if k == 0:
        if any(c == 1 for c in cur): return None
        return [0] * n
    r = rec(0, 0)
    if r is None: return None
    a1, a0 = r
    out = []
    for j in range(n):
        if a1[j] and not a0[j]: out.append(1)
        elif a0[j] and not a1[j]: out.append(0)
        elif not a1[j] and not a0[j]: return None
        else: out.append(-1)
    return out

def solve(rows, cols, n):
    g = [[-1] * n for _ in range(n)]
    passes = 0; changed = True
    while changed:
        changed = False; passes += 1
        for y in range(n):
            r = line_solve(rows[y], g[y], n)
            if r is None: return None, passes
            for x in range(n):
                if r[x] != -1 and g[y][x] == -1: g[y][x] = r[x]; changed = True
        for x in range(n):
            col = [g[y][x] for y in range(n)]
            r = line_solve(cols[x], col, n)
            if r is None: return None, passes
            for y in range(n):
                if r[y] != -1 and g[y][x] == -1: g[y][x] = r[y]; changed = True
        if passes > 60: break
    done = all(v != -1 for row in g for v in row)
    return (g if done else None), passes

# ---------------- 품질 검사 ----------------
def good(G):
    n = G.shape[0]; d = G.mean()
    if not (0.32 <= d <= 0.74): return False
    empty = sum(1 for r in G if not r.any()) + sum(1 for c in G.T if not c.any())
    full = sum(1 for r in G if r.all()) + sum(1 for c in G.T if c.all())
    if empty > 1 or full > max(2, n // 3): return False
    # 너무 잘게 흩어진 무늬(체크무늬) 방지
    Gi = G.astype(int)
    flips = np.abs(np.diff(Gi, axis=1)).sum() + np.abs(np.diff(Gi, axis=0)).sum()
    if flips > 1.15 * n * n: return False
    return True

def variants(G):
    out = []
    for k in range(4):
        R = np.rot90(G, k); out.append(R); out.append(R[:, ::-1])
    return out

def key(G):
    return min(''.join(map(str, v.flatten().tolist())) for v in variants(G))

# ---------------- 출처 1: 게임 그림 축소 ----------------
NAMES = json.load(open(os.path.join(os.path.dirname(__file__), 'names.json'), encoding='utf-8'))

def from_alpha(path, n, thr, detail=False):
    """물건 그림 → n×n. 모양을 칸에 꽉 차게 늘리고, detail 이면 어두운 무늬(창문·눈·줄무늬)를 빈칸으로."""
    im = Image.open(path).convert('RGBA')
    A = np.asarray(im).astype(float)
    a = A[..., 3] / 255
    ys, xs = np.where(a > 0.3)
    if len(ys) == 0: return None
    A = A[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = A.shape[:2]
    # 너무 길쭉하면 짧은 쪽만 조금 여유를 두고 늘림
    if max(h, w) / min(h, w) > 1.6:
        s_ = max(h, w); t = int(min(h, w) * 1.25)
        P = np.zeros((s_ if h >= w else t, t if h >= w else s_, 4)); oy = (P.shape[0] - h) // 2; ox = (P.shape[1] - w) // 2
        P[oy:oy + h, ox:ox + w] = A; A = P
    img = Image.fromarray(A.clip(0, 255).astype('uint8'), 'RGBA').resize((n, n), Image.BOX)
    S = np.asarray(img).astype(float)
    G = (S[..., 3] / 255 > thr)
    if detail:
        lum = S[..., :3].mean(2); inside = G
        if inside.sum() > 4:
            m = lum[inside].mean(); sd = lum[inside].std()
            G = G & ~(lum < m - .9 * sd)
    return G.astype(np.uint8)

def sprite_pictures():
    files = sorted(glob.glob(os.path.join(ROOT, 'img/sprites/*.webp')) + glob.glob(os.path.join(ROOT, 'img/voyage/*.webp')))
    pics = []
    for f in files:
        nm = os.path.basename(f).rsplit('.', 1)[0]
        label = NAMES.get(nm)
        if not label: continue
        pics.append((f, label))
    return pics

# ---------------- 출처 2: 도형 ----------------
def shape(kind, n, t):
    S = n * 8; im = Image.new('L', (S, S), 0); d = ImageDraw.Draw(im); c = S / 2; r = S * 0.46
    def poly(pts): d.polygon([(c + x * r, c + y * r) for x, y in pts], fill=255)
    if kind == 'heart':
        d.ellipse([c - r, c - r * .75, c, c + r * .1], fill=255); d.ellipse([c, c - r * .75, c + r, c + r * .1], fill=255)
        poly([(-0.98, -0.2), (0.98, -0.2), (0, 0.98)])
    elif kind == 'star':
        pts = [((1 if i % 2 == 0 else .45) * math.cos(-math.pi / 2 + i * math.pi / 5), (1 if i % 2 == 0 else .45) * math.sin(-math.pi / 2 + i * math.pi / 5) + .08) for i in range(10)]; poly(pts)
    elif kind == 'diamond': poly([(0, -1), (.8, 0), (0, 1), (-.8, 0)])
    elif kind == 'ring':
        d.ellipse([c - r, c - r, c + r, c + r], fill=255); rr = r * (.45 + .15 * t); d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=0)
    elif kind == 'moon':
        d.ellipse([c - r, c - r, c + r, c + r], fill=255); o = r * (.45 + .2 * t); d.ellipse([c - r + o, c - r - o * .3, c + r + o, c + r - o * .3], fill=0)
    elif kind == 'arrow': poly([(0, -1), (.9, -.1), (.35, -.1), (.35, 1), (-.35, 1), (-.35, -.1), (-.9, -.1)])
    elif kind == 'cross': d.rectangle([c - r * .32, c - r, c + r * .32, c + r], fill=255); d.rectangle([c - r, c - r * .32, c + r, c + r * .32], fill=255)
    elif kind == 'house': poly([(0, -1), (1, -.1), (.75, -.1), (.75, 1), (-.75, 1), (-.75, -.1), (-1, -.1)]); d.rectangle([c - r * .2, c + r * .35, c + r * .2, c + r], fill=0)
    elif kind == 'tree': poly([(0, -1), (.8, .45), (-.8, .45)]); d.rectangle([c - r * .18, c + r * .4, c + r * .18, c + r], fill=255)
    elif kind == 'drop': d.ellipse([c - r * .75, c - r * .2, c + r * .75, c + r], fill=255); poly([(0, -1), (.66, .2), (-.66, .2)])
    elif kind == 'bolt': poly([(.25, -1), (-.6, .1), (-.05, .1), (-.3, 1), (.6, -.15), (.05, -.15)])
    elif kind == 'key':
        d.ellipse([c - r, c - r * .55, c - r * .1, c + r * .35], fill=255); d.ellipse([c - r * .75, c - r * .3, c - r * .35, c + r * .1], fill=0)
        d.rectangle([c - r * .15, c - r * .2, c + r, c + r * .05], fill=255); d.rectangle([c + r * .55, c, c + r * .75, c + r * .45], fill=255); d.rectangle([c + r * .8, c, c + r, c + r * .3], fill=255)
    elif kind == 'flower':
        for i in range(5):
            a = -math.pi / 2 + i * 2 * math.pi / 5; x, y = c + math.cos(a) * r * .55, c + math.sin(a) * r * .55
            d.ellipse([x - r * .42, y - r * .42, x + r * .42, y + r * .42], fill=255)
        d.ellipse([c - r * .25, c - r * .25, c + r * .25, c + r * .25], fill=0 if t > .5 else 255)
    elif kind == 'cat':
        d.ellipse([c - r * .85, c - r * .55, c + r * .85, c + r * .95], fill=255); poly([(-.85, -.2), (-.75, -1), (-.2, -.5)]); poly([(.85, -.2), (.75, -1), (.2, -.5)])
        for sx in (-.35, .35): d.ellipse([c + sx * r - r * .12, c + r * .1, c + sx * r + r * .12, c + r * .35], fill=0)
    elif kind == 'fish':
        d.ellipse([c - r * .9, c - r * .55, c + r * .45, c + r * .55], fill=255); poly([(.3, 0), (1, -.6), (1, .6)]); d.ellipse([c - r * .55, c - r * .2, c - r * .3, c + r * .05], fill=0)
    elif kind == 'mushroom':
        d.pieslice([c - r, c - r * .9, c + r, c + r * .7], 180, 360, fill=255); d.rectangle([c - r * .35, c - r * .1, c + r * .35, c + r], fill=255)
        d.ellipse([c - r * .5, c - r * .65, c - r * .2, c - r * .35], fill=0); d.ellipse([c + r * .15, c - r * .7, c + r * .45, c - r * .4], fill=0)
    elif kind == 'cup':
        d.rectangle([c - r * .7, c - r * .5, c + r * .4, c + r * .8], fill=255); d.ellipse([c + r * .2, c - r * .3, c + r, c + r * .5], fill=255); d.ellipse([c + r * .4, c - r * .1, c + r * .75, c + r * .3], fill=0)
        d.rectangle([c - r * .5, c - r * .3, c + r * .2, c + r * .6], fill=0 if t > .5 else 255)
    elif kind == 'smile':
        d.ellipse([c - r, c - r, c + r, c + r], fill=255)
        for sx in (-.38, .38): d.ellipse([c + sx * r - r * .14, c - r * .45, c + sx * r + r * .14, c - r * .1], fill=0)
        d.arc([c - r * .55, c - r * .35, c + r * .55, c + r * .6], 20, 160, fill=0, width=max(2, int(S / n)))
    small = np.asarray(im.resize((n, n), Image.BOX)).astype(float) / 255
    return (small > .45 + .1 * (t - .5)).astype(np.uint8)

SHAPES = {'heart': '하트', 'star': '별', 'diamond': '다이아몬드', 'ring': '반지', 'moon': '초승달', 'arrow': '화살표', 'cross': '십자', 'house': '집',
          'tree': '나무', 'drop': '물방울', 'bolt': '번개', 'key': '열쇠', 'flower': '꽃', 'cat': '고양이', 'fish': '물고기', 'mushroom': '버섯', 'cup': '머그컵', 'smile': '웃는 얼굴'}

# ---------------- 출처 3: 무늬 ----------------
def pattern(n, kind):
    p = rng.uniform(.45, .62)
    if kind == 'mirror':
        G = (np.random.default_rng(rng.randrange(1 << 30)).random((n, (n + 1) // 2)) < p).astype(np.uint8)
        return np.hstack([G, G[:, :n // 2][:, ::-1]])
    if kind == 'vmirror': return pattern(n, 'mirror').T.copy()
    if kind == 'rot':
        R = np.random.default_rng(rng.randrange(1 << 30)).random((n, n)) < p; G = np.zeros((n, n), np.uint8)
        for y in range(n):
            for x in range(n):
                if y * n + x <= (n - 1 - y) * n + (n - 1 - x): G[y, x] = G[n - 1 - y, n - 1 - x] = R[y, x]
        return G
    if kind == 'quad':
        h = (n + 1) // 2; Q = (np.random.default_rng(rng.randrange(1 << 30)).random((h, h)) < p).astype(np.uint8)
        top = np.hstack([Q, Q[:, :n // 2][:, ::-1]]); return np.vstack([top, top[:n // 2][::-1]])
    # 비대칭 덩어리: 무작위 → 이웃 다수결로 다듬기
    G = (np.random.default_rng(rng.randrange(1 << 30)).random((n, n)) < p).astype(np.uint8)
    for _ in range(rng.choice([1, 2, 2, 3])):
        P = np.pad(G, 1); S = sum(P[1 + dy:1 + dy + n, 1 + dx:1 + dx + n] for dy in (-1, 0, 1) for dx in (-1, 0, 1))
        G = (S >= 5).astype(np.uint8) | ((S == 4) & (G == 1)).astype(np.uint8)
    return G

# ---------------- 예전 그림 ----------------
def old_pics():
    s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    a = s.index('const PICS=') + len('const PICS='); b = s.index('\n};', a) + 2
    txt = re.sub(r'(\n\s*)(\d+):', r'\1"\2":', s[a:b].replace("'", '"'))
    out = []
    for k, v in json.loads(txt).items():
        for p in v: out.append((int(k), np.array([[1 if ch == '#' else 0 for ch in row] for row in p], np.uint8)))
    return out

# ---------------- 모으기 ----------------
def build():
    sprites = sprite_pictures()
    olds = old_pics()
    bank = {}; report = {}
    for n in SIZES:
        seen = set(); kept = []  # (G, label, source, passes)
        def offer(G, label, src):
            if G is None or G.shape != (n, n) or not good(G): return False
            k = key(G)
            if k in seen: return False
            flat = G.flatten()
            for H, *_ in kept:
                if min(np.sum(v.flatten() != flat) for v in variants(H)) < max(3, n * n * .12): return False
            rows = [clue(r) for r in G.tolist()]; cols = [clue(c) for c in G.T.tolist()]
            sol, passes = solve(rows, cols, n)
            if sol is None or (np.array(sol) != G).any(): return False
            seen.add(k); kept.append((G, label, src, passes)); return True
        for k, G in olds:
            if k == n: offer(G, '', 'old')
        # 그림 (물건) — 작은 크기에서는 알아보기 어려워 크기 7 이상에서 많이
        order = sprites[:]; rng.shuffle(order)
        for f, label in order:
            done = False
            for detail in ((True, False) if n >= 8 else (False, True)):
                for thr in (.5, .42, .58):
                    if offer(from_alpha(f, n, thr, detail), label, 'pic'): done = True; break
                if done: break
        for kind, label in SHAPES.items():
            for t in (.5, .2, .8):
                if offer(shape(kind, n, t), label, 'shape'): break
        kinds = ['mirror', 'vmirror', 'rot', 'quad', 'blob', 'blob']
        tries = 0
        while len(kept) < POOL and tries < 40000:
            tries += 1; offer(pattern(n, kinds[tries % len(kinds)]), '', 'pat')
        # 출처를 섞어서 순서 정하기: 쉬운(추론 횟수 적은) 것부터, 같은 출처가 연달아 나오지 않게
        kept.sort(key=lambda t: t[3] + rng.random() * 2)
        pics = [t for t in kept if t[2] != 'pat']; pats = [t for t in kept if t[2] == 'pat']
        mixed = []
        while pics or pats:
            if pics and (not pats or len(mixed) % 2 == 0): mixed.append(pics.pop(0))
            elif pats: mixed.append(pats.pop(0))
        mixed = mixed[:POOL]
        bank[n] = mixed
        report[n] = {'total': len(mixed), 'pic': sum(t[2] == 'pic' for t in mixed), 'shape': sum(t[2] == 'shape' for t in mixed),
                     'old': sum(t[2] == 'old' for t in mixed), 'pattern': sum(t[2] == 'pat' for t in mixed)}
    return bank, report

def encode(G):
    return ''.join(format(int(''.join(map(str, r)), 2), 'x').zfill((len(r) + 3) // 4) for r in G.tolist())

if __name__ == '__main__':
    bank, report = build()
    data = {n: [encode(G) + ('|' + lab if lab else '') for G, lab, src, ps in bank[n]] for n in SIZES}
    js = 'const LOGIC_BANK=' + json.dumps({str(k): ','.join(v) for k, v in data.items()}, ensure_ascii=False) + ';'
    p = os.path.join(ROOT, 'index.html'); s = open(p, encoding='utf-8').read()
    A, B = '/*LOGIC_BANK*/', '/*/LOGIC_BANK*/'
    if A in s:
        i = s.index(A); j = s.index(B) + len(B); s = s[:i] + A + js + B + s[j:]
    else:
        s = s.replace('const PICS={', A + js + B + '\nconst PICS={', 1)
    open(p, 'w', encoding='utf-8').write(s)
    print(json.dumps(report, ensure_ascii=False))
    print('bytes', len(js))
