"""그림과 랭킹 설정을 모두 안에 넣은 HTML 파일 하나를 만든다.

사용법: python3 tools/build_single.py  →  dist/틀린로직맞추기.html
"""
import base64
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

html = open('index.html', encoding='utf-8').read()
embed = {}
for f in sorted(glob.glob('img/*/*.png') + glob.glob('img/*/*.jpg')):
    mime = 'image/png' if f.endswith('.png') else 'image/jpeg'
    embed[f] = f'data:{mime};base64,' + base64.b64encode(open(f, 'rb').read()).decode()

tag = '<script src="rank-config.js"></script>'
assert html.count(tag) == 1, 'rank-config.js 태그를 찾지 못함'
html = html.replace(tag, '<script>\n' + open('rank-config.js', encoding='utf-8').read() + '\n</script>')
i = html.index('<script>')
html = html[:i] + '<script>window.SEKAN_EMBED=' + json.dumps(embed) + ';</script>\n' + html[i:]

os.makedirs('dist', exist_ok=True)
out = 'dist/틀린로직맞추기.html'
open(out, 'w', encoding='utf-8').write(html)
print(f'{out}: 그림 {len(embed)}개, {os.path.getsize(out) // 1024} KB')
