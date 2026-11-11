"""과자 나라 301~600 문제집 (11×11 150개 + 12×12 150개) — 패치 6.6.

기존 1~300(gen.py)은 그대로 두고 뒤에 붙인다. 구역·답 한 칸을 36진수 한 글자(0-9a-z)로 적어
11·12 크기도 한 글자씩이다(기존 0~9 코드와 그대로 호환).
  301~350  11×11  기법 lv≥2(앞서 보기)
  351~450  11×11  기법 lv≥3(구역 묶어 보기)
  451~600  12×12  기법 lv≥3
쉬운 것부터 어려운 것 순으로 고르게 솎아 넣는다. 병렬(4코어)로 1시간쯤 걸린다.
사용법: python3 tools/candy/gen_ext.py [--out 파일.json] [--apply]
  --apply 를 주면 결과를 index.html 의 /*CANDY_BANK*/ 블록 뒤에 붙인다(이미 600개면 건너뜀).
"""
import sys, os, json, random, time, math, re
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen

B36 = '0123456789abcdefghijklmnopqrstuvwxyz'
BLOCKS = [(11, 2, 50, 1.4), (11, 3, 100, 1.3), (12, 3, 150, 1.25)]   # (크기, 최소 기법, 개수, 후보 배수)


def enc(reg, sol):
    return ''.join(B36[k] for k in reg) + ''.join(B36[q] for q in sol)


def work(a):
    N, lvmin, seed = a
    rnd = random.Random(seed)
    reg, sol, sc, lv, ez = gen.make(N, rnd, lambda l, s, e: l >= lvmin)
    return N, lvmin, sc + lv * 6, enc(reg, sol), gen.canon(N, reg)


def main():
    out = 'bank_ext.json'
    if '--out' in sys.argv: out = sys.argv[sys.argv.index('--out') + 1]
    if os.path.exists(out):
        res = json.load(open(out, encoding='utf-8'))
    else:
        res = {}
    t0 = time.time()
    pool = Pool(int(os.environ.get('GEN_PROCS', '3')))
    for bi, (N, lv, cnt, mult) in enumerate(BLOCKS):
        key = f'{N}_{lv}_{cnt}'
        if key in res and len(res[key]) >= cnt:
            continue
        n = math.ceil(cnt * mult)
        tasks = [(N, lv, 20261111 + bi * 100000 + i) for i in range(n)]
        got, seen = [], set()
        for k, r in enumerate(pool.imap_unordered(work, tasks), 1):
            if r[4] in seen: continue
            seen.add(r[4]); got.append((r[2], r[3]))
            if k % 10 == 0:
                print(f'{key} {k}/{n} {time.time() - t0:.0f}s', file=sys.stderr, flush=True)
        got.sort()
        step = len(got) / cnt
        res[key] = [got[int(i * step)][1] for i in range(cnt)]
        json.dump(res, open(out, 'w', encoding='utf-8'))
        print(f'{key} 끝: 점수 {got[0][0]}→{got[-1][0]} {time.time() - t0:.0f}s', file=sys.stderr, flush=True)
    pool.close()
    if '--apply' in sys.argv:
        apply(res)


def apply(res):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'index.html')
    html = open(path, encoding='utf-8').read()
    m = re.search(r'/\*CANDY_BANK\*/const CANDY_BANK=(.*?);/\*/CANDY_BANK\*/', html, flags=re.S)
    bank = json.loads(m.group(1))
    rounds = bank['r'].split(',')
    if len(rounds) >= 600:
        print('이미 600개:', len(rounds)); return
    assert len(rounds) == 300
    for N, lv, cnt, mult in BLOCKS:
        rounds += res[f'{N}_{lv}_{cnt}']
    assert len(rounds) == 600
    bank['r'] = ','.join(rounds)
    js = '/*CANDY_BANK*/const CANDY_BANK=' + json.dumps(bank, separators=(',', ':')) + ';/*/CANDY_BANK*/'
    html = html[:m.start()] + js + html[m.end():]
    open(path, 'w', encoding='utf-8').write(html)
    print('index.html 문제집 갱신', len(js))


if __name__ == '__main__':
    main()
