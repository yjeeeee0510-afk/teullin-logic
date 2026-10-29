"""과자 나라 문제집 만들기 (스타배틀 1개짜리 = Meowdoku 방식).

규칙: N×N 판, N개 색 구역. 가로줄·세로줄·구역마다 친구 한 명, 친구끼리 옆·대각선으로 붙지 않음.
모든 문제는 아래 추론만으로 끝까지 풀린다(= 답이 하나).
  0 기본: 친구 자리 주변·같은 줄·같은 구역 지우기, 후보가 하나 남은 줄·구역은 그 칸
  1 한 줄에 갇힌 구역: 구역 후보가 한 가로/세로줄에만 있으면 그 줄의 다른 칸 지우기 (반대도)
  2 앞서 보기: 이 칸에 앉히면 어떤 줄·구역에 자리가 하나도 안 남으면 그 칸 지우기
  3 묶어 보기: k개 구역 후보가 k개 줄 안에만 있으면 그 줄들의 다른 칸 지우기 (k=2,3)
사용법: python3 tools/candy/gen.py  → index.html 의 /*CANDY_BANK*/ 블록을 바꾼다
"""
import random, itertools, re, sys, os, json

def neighbors(N):
    nb = []
    for c in range(N * N):
        r, q = divmod(c, N)
        nb.append([rr * N + qq for rr in range(r - 1, r + 2) for qq in range(q - 1, q + 2)
                   if 0 <= rr < N and 0 <= qq < N and (rr, qq) != (r, q)])
    return nb

def solve(N, reg, nb):
    """추론으로 풀기. (풀렸는가, 단계 점수, 가장 어려운 기법, 첫 칸이 바로 보이는가)"""
    rows = [[r * N + q for q in range(N)] for r in range(N)]
    cols = [[r * N + q for r in range(N)] for q in range(N)]
    regs = [[c for c in range(N * N) if reg[c] == k] for k in range(N)]
    units = rows + cols + regs
    cand = set(range(N * N)); star = set()
    score = 0; level = 0; first_easy = None

    def place(c):
        star.add(c)
        r, q = divmod(c, N)
        kill = set(rows[r]) | set(cols[q]) | set(regs[reg[c]]) | set(nb[c])
        cand.difference_update(kill)

    def unit_open(u):
        return not any(c in star for c in u)

    while len(star) < N:
        # 0: 후보가 하나뿐인 줄·구역
        hit = None
        for u in units:
            if unit_open(u):
                cs = [c for c in u if c in cand]
                if not cs: return False, score, level, first_easy, -1
                if len(cs) == 1: hit = cs[0]; break
        if hit is not None:
            if first_easy is None: first_easy = True
            place(hit); score += 1; continue
        if first_easy is None: first_easy = False
        # 1: 한 줄에 갇힌 구역 / 한 구역에 갇힌 줄
        done = False
        for k in range(N):
            if not unit_open(regs[k]): continue
            cs = [c for c in regs[k] if c in cand]
            rs = {c // N for c in cs}; qs = {c % N for c in cs}
            for lines, idx in ((rows, rs), (cols, qs)):
                if len(idx) == 1:
                    i = next(iter(idx))
                    rm = [c for c in lines[i] if c in cand and reg[c] != k]
                    if rm: cand.difference_update(rm); done = True
        for lines in (rows, cols):
            for u in lines:
                if not unit_open(u): continue
                cs = [c for c in u if c in cand]
                ks = {reg[c] for c in cs}
                if len(ks) == 1:
                    k = next(iter(ks))
                    rm = [c for c in regs[k] if c in cand and c not in u]
                    if rm: cand.difference_update(rm); done = True
        if done: score += 2; level = max(level, 1); continue
        # 2: 앞서 보기
        rm = []
        for c in list(cand):
            r, q = divmod(c, N)
            kill = set(rows[r]) | set(cols[q]) | set(regs[reg[c]]) | set(nb[c])
            for u in units:
                if c in u or not unit_open(u): continue
                if not any(x in cand and x not in kill for x in u):
                    rm.append(c); break
        if rm: cand.difference_update(rm); score += 5; level = max(level, 2); continue
        if pigeon(N, 2, rows, cols, regs, reg, cand, star):
            score += 7; level = max(level, 3); continue
        if pigeon(N, 3, rows, cols, regs, reg, cand, star):
            score += 9; level = max(level, 3); continue
        return False, score, level, first_easy, len(star) * N * N + (N * N - len(cand))
    return True, score, level, first_easy, 10 ** 6

def pigeon(N, k, rows, cols, regs, reg, cand, star):
    openreg = [i for i in range(N) if not any(c in star for c in regs[i])]
    for lines, key in ((rows, lambda c: c // N), (cols, lambda c: c % N)):
        # k개 구역의 후보가 k개 줄 안에만
        for combo in itertools.combinations(openreg, k):
            cs = [c for i in combo for c in regs[i] if c in cand]
            idx = {key(c) for c in cs}
            if len(idx) == k:
                rm = [c for i in idx for c in lines[i] if c in cand and reg[c] not in combo]
                if rm: cand.difference_update(rm); return True
        # k개 줄의 후보가 k개 구역 안에만
        openl = [i for i in range(N) if not any(c in star for c in lines[i])]
        for combo in itertools.combinations(openl, k):
            cs = [c for i in combo for c in lines[i] if c in cand]
            ks = {reg[c] for c in cs}
            if len(ks) == k:
                rm = [c for kk in ks for c in regs[kk] if c in cand and key(c) not in combo]
                if rm: cand.difference_update(rm); return True
    return False

def rand_solution(N, rnd):
    while True:
        p = []
        ok = True
        for r in range(N):
            opts = [q for q in range(N) if q not in p and (not p or abs(q - p[-1]) > 1)]
            if not opts: ok = False; break
            p.append(rnd.choice(opts))
        if ok: return p

def grow_regions(N, sol, rnd, spread):
    reg = [-1] * (N * N)
    front = []
    for r, q in enumerate(sol):
        c = r * N + q; reg[c] = r; front.append(c)
    left = N * N - N
    sizes = [1] * N
    while left:
        # 작은 구역을 조금 더 자주 키운다(spread가 클수록 크기가 고르지 않음)
        k = rnd.choices(range(N), weights=[1.0 / (s ** spread) for s in sizes])[0]
        border = []
        for c in range(N * N):
            if reg[c] != k: continue
            r, q = divmod(c, N)
            for rr, qq in ((r - 1, q), (r + 1, q), (r, q - 1), (r, q + 1)):
                if 0 <= rr < N and 0 <= qq < N and reg[rr * N + qq] == -1:
                    border.append(rr * N + qq)
        if not border:
            sizes[k] = 10 ** 6; continue
        c = rnd.choice(border); reg[c] = k; sizes[k] += 1; left -= 1
    return reg

def connected(N, reg, k, without):
    cells = [c for c in range(N * N) if reg[c] == k and c != without]
    if not cells: return False
    seen = {cells[0]}; st = [cells[0]]; cs = set(cells)
    while st:
        c = st.pop(); r, q = divmod(c, N)
        for rr, qq in ((r - 1, q), (r + 1, q), (r, q - 1), (r, q + 1)):
            x = rr * N + qq
            if 0 <= rr < N and 0 <= qq < N and x in cs and x not in seen:
                seen.add(x); st.append(x)
    return len(seen) == len(cells)

def mutate(N, reg, stars, rnd):
    for _ in range(50):
        c = rnd.randrange(N * N)
        if c in stars: continue
        r, q = divmod(c, N)
        nbk = {reg[rr * N + qq] for rr, qq in ((r - 1, q), (r + 1, q), (r, q - 1), (r, q + 1))
               if 0 <= rr < N and 0 <= qq < N} - {reg[c]}
        if not nbk: continue
        if not connected(N, reg, reg[c], c): continue
        new = reg[:]; new[c] = rnd.choice(sorted(nbk))
        return new
    return None

def make(N, rnd, want, steps=None):
    nb = neighbors(N)
    steps = steps or 60 * N * N
    while True:
        sol = rand_solution(N, rnd)
        stars = {r * N + q for r, q in enumerate(sol)}
        reg = grow_regions(N, sol, rnd, spread=rnd.choice([0.6, 1.0, 1.5]))
        res = solve(N, reg, nb); best = res[4]
        for _ in range(steps):
            if res[0]: break
            new = mutate(N, reg, stars, rnd)
            if new is None: break
            r2 = solve(N, new, nb)
            if r2[4] >= best:
                reg, res, best = new, r2, r2[4]
        ok, score, level, easy, _ = res
        if ok and want(level, score, easy):
            return reg, sol, score, level, easy

def canon(N, reg):
    # 구역 번호를 처음 나온 순서로 다시 매겨 같은 판 찾기
    m = {}; out = []
    for k in reg:
        if k not in m: m[k] = len(m)
        out.append(m[k])
    return tuple(out)

def encode(N, reg, sol):
    # 구역은 칸마다 한 글자(0~9), 답은 줄마다 칸 번호
    return ''.join(str(k) for k in reg) + ''.join(str(q) for q in sol)

# 라운드 구성: (크기, 개수, 기법 조건)
PLAN = [
    (5, 30, lambda lv, sc, ez: lv == 0 and ez),
    (6, 30, lambda lv, sc, ez: lv <= 1),
    (6, 20, lambda lv, sc, ez: lv >= 1),
    (7, 20, lambda lv, sc, ez: lv >= 1),
    (7, 40, lambda lv, sc, ez: lv >= 1),
    (8, 60, lambda lv, sc, ez: lv >= 1),
    (8, 25, lambda lv, sc, ez: lv >= 2),
    (9, 25, lambda lv, sc, ez: lv >= 2),
    (9, 25, lambda lv, sc, ez: lv >= 2),
    (10, 25, lambda lv, sc, ez: lv >= 2),
]
DAILY = {6: 30, 7: 30, 8: 30, 9: 30}

if __name__ == '__main__':
    rnd = random.Random(20261029)
    seen = set()
    rounds = []
    for N, cnt, want in PLAN:
        got = []
        tries = 0
        while len(got) < int(cnt * 1.5) and tries < cnt * 6:
            tries += 1
            reg, sol, sc, lv, ez = make(N, rnd, want)
            key = canon(N, reg)
            if key in seen: continue
            seen.add(key); got.append((sc + lv * 6, encode(N, reg, sol)))
        got.sort()
        # 쉬운 것부터, 두 배 뽑아 고르게 솎기
        step = len(got) / cnt
        pickd = [got[int(i * step)][1] for i in range(cnt)]
        rounds += pickd
        print(N, cnt, 'score', got[0][0], '→', got[-1][0], file=sys.stderr)
    assert len(rounds) == 300, len(rounds)
    daily = {}
    for N, cnt in DAILY.items():
        arr = []
        while len(arr) < cnt:
            reg, sol, sc, lv, ez = make(N, rnd, lambda lv, sc, ez: lv >= (1 if N < 8 else 2))
            key = canon(N, reg)
            if key in seen: continue
            seen.add(key); arr.append(encode(N, reg, sol))
        daily[N] = ','.join(arr)
    bank = {'r': ','.join(rounds), 'd': daily}
    js = '/*CANDY_BANK*/const CANDY_BANK=' + json.dumps(bank, separators=(',', ':')) + ';/*/CANDY_BANK*/'
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'index.html')
    html = open(path, encoding='utf-8').read()
    if '/*CANDY_BANK*/' in html:
        html = re.sub(r'/\*CANDY_BANK\*/.*?/\*/CANDY_BANK\*/', lambda m: js, html, flags=re.S)
        open(path, 'w', encoding='utf-8').write(html)
        print('index.html 문제집 갱신', len(js), file=sys.stderr)
    else:
        open(os.path.join(os.path.dirname(__file__), 'bank.js'), 'w').write(js)
        print('bank.js 저장 (index.html에 /*CANDY_BANK*/ 블록이 아직 없음)', len(js), file=sys.stderr)
