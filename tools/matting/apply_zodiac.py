"""십이지 리뉴얼(Z1~Z4) 누끼 → index.html 의 ZIMG(base64 WebP) 교체.
먼저 `python3 tools/matting/chroma.py Z1 Z2 Z3 Z4` 로 tools/matting/out/zFace0~11·zBody0~11.webp 를 만든다.
얼굴: 220×220 정사각형 가운데(긴 쪽 220). 몸: 높이 213, 너비는 비율대로(최대 220). 순서는 ZODIAC.NAMES.
"""
import os, io, re, base64
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'tools', 'matting', 'out')


def uri(im):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=90, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def face(i):
    im = Image.open(os.path.join(OUT, f'zFace{i}.webp')).convert('RGBA')
    im = im.crop(im.getchannel('A').getbbox())
    s = 220 / max(im.size); im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    c = Image.new('RGBA', (220, 220), (0, 0, 0, 0)); c.paste(im, ((220 - im.width) // 2, (220 - im.height) // 2), im)
    return c


def body(i):
    im = Image.open(os.path.join(OUT, f'zBody{i}.webp')).convert('RGBA')
    im = im.crop(im.getchannel('A').getbbox())
    s = min(213 / im.height, 220 / im.width)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def main():
    js = 'const ZIMG={body:[' + ','.join(f'"{uri(body(i))}"' for i in range(12)) + '],face:[' + ','.join(f'"{uri(face(i))}"' for i in range(12)) + ']};'
    p = os.path.join(ROOT, 'index.html'); s = open(p, encoding='utf-8').read()
    i = s.index('const ZIMG={'); j = s.index('};', i) + 2
    s = s[:i] + js + s[j:]
    open(p, 'w', encoding='utf-8').write(s)
    print('ZIMG', len(js), 'bytes')


if __name__ == '__main__':
    main()
