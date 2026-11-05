"""안드로이드 앱 새로 만들어 올리기 준비 (5.8~).

python3 tools/app/release.py
 1) www 복사 → cap sync → gradle assembleRelease bundleRelease (ANDROID_HOME 필요, 서명 키 app/android/keystore.properties)
 2) APK → download/teullinlogic.apk
 3) version.json(version·code·size·notes·date) 작성 — 앱이 켜질 때 이걸 보고 '새 버전이 나왔어요' 안내
    (download.html도 이 파일을 읽어 버전·용량을 보여 줌)
그다음 커밋·푸시하면 끝.
"""
import os, re, json, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP = os.path.join(ROOT, 'app')
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
m = re.search(r'id="introVer"[^>]*>패치 (\d+)\.(\d)', html)
ver = f'{m.group(1)}.{m.group(2)}'; code = int(m.group(1)) * 10 + int(m.group(2))
pn = re.search(r"\[\s*'%s'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*\[(.*?)\]\s*\]" % re.escape(ver), html, re.S)
date, title, notes = (pn.group(1), pn.group(2), re.findall(r"'([^']*)'", pn.group(3))) if pn else ('', '', [])
if '--skip-build' not in sys.argv:
    run = lambda c, d: subprocess.run(c, cwd=d, shell=True, check=True)
    run('node copy-web.mjs', APP)
    run('npx cap sync android', APP)
    run('./gradlew -q assembleRelease bundleRelease', os.path.join(APP, 'android'))
apk = os.path.join(APP, 'android', 'app', 'build', 'outputs', 'apk', 'release', 'app-release.apk')
dst = os.path.join(ROOT, 'download', 'teullinlogic.apk'); shutil.copy(apk, dst)
size = f'{os.path.getsize(dst) / 1048576:.1f}MB'
info = {'version': ver, 'code': code, 'size': size, 'date': date, 'title': title, 'notes': notes, 'apk': 'download/teullinlogic.apk'}
json.dump(info, open(os.path.join(ROOT, 'version.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# download.html 기본 글자(파일을 못 읽을 때 보임)도 맞춤
p = os.path.join(ROOT, 'download.html'); d = open(p, encoding='utf-8').read()
d = re.sub(r'버전 [\d.]+ · [\d.]+MB', f'버전 {ver} · {size}', d); open(p, 'w', encoding='utf-8').write(d)
print('준비 완료:', info)
