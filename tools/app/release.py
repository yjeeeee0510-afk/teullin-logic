"""안드로이드 앱 새로 만들어 올리기 준비 (5.8~).

두 가지 배포 경로(Gradle 플레이버):
  sideload — 다운로드 페이지판 APK(자체 업데이트 O). 기본.
  play     — 구글 플레이용 AAB(자체 업데이트·권한 없음).

python3 tools/app/release.py            # sideload: APK → download/teullinlogic.apk + version.json·download.html
python3 tools/app/release.py --play     # play:     AAB → dist/teullinlogic-play.aab (커밋 안 함, 콘솔에 업로드)
  (ANDROID_HOME 필요, 서명 키 app/android/keystore.properties)
  --skip-build 로 빌드 건너뛰고 뒷정리만.
"""
import os, re, json, shutil, subprocess, sys
PLAY = '--play' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP = os.path.join(ROOT, 'app')
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
m = re.search(r'id="introVer"[^>]*>패치 (\d+)\.(\d)', html)
ver = f'{m.group(1)}.{m.group(2)}'; code = int(m.group(1)) * 10 + int(m.group(2))
pn = re.search(r"\[\s*'%s'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*\[(.*?)\]\s*\]" % re.escape(ver), html, re.S)
date, title, notes = (pn.group(1), pn.group(2), re.findall(r"'([^']*)'", pn.group(3))) if pn else ('', '', [])
run = lambda c, d, env=None: subprocess.run(c, cwd=d, shell=True, check=True, env=env)

if PLAY:
    if '--skip-build' not in sys.argv:
        run('node copy-web.mjs', APP, {**os.environ, 'PLAY': '1'})   # 구글 플레이 판 표시 주입
        run('npx cap sync android', APP)
        run('./gradlew -q bundlePlayRelease', os.path.join(APP, 'android'))
    aab = os.path.join(APP, 'android', 'app', 'build', 'outputs', 'bundle', 'playRelease', 'app-play-release.aab')
    os.makedirs(os.path.join(ROOT, 'dist'), exist_ok=True)
    dst = os.path.join(ROOT, 'dist', 'teullinlogic-play.aab'); shutil.copy(aab, dst)
    size = f'{os.path.getsize(dst) / 1048576:.1f}MB'
    print(f'구글 플레이 AAB 준비 완료: {dst}  (패치 {ver} · versionCode {code} · {size})')
    print('→ Play Console에 이 .aab 파일을 업로드하세요. (version.json·download.html은 건드리지 않음)')
else:
    if '--skip-build' not in sys.argv:
        run('node copy-web.mjs', APP)
        run('npx cap sync android', APP)
        run('./gradlew -q assembleSideloadRelease', os.path.join(APP, 'android'))
    apk = os.path.join(APP, 'android', 'app', 'build', 'outputs', 'apk', 'sideload', 'release', 'app-sideload-release.apk')
    dst = os.path.join(ROOT, 'download', 'teullinlogic.apk'); shutil.copy(apk, dst)
    size = f'{os.path.getsize(dst) / 1048576:.1f}MB'
    info = {'version': ver, 'code': code, 'size': size, 'date': date, 'title': title, 'notes': notes, 'apk': 'download/teullinlogic.apk'}
    json.dump(info, open(os.path.join(ROOT, 'version.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # download.html 기본 글자(파일을 못 읽을 때 보임)도 맞춤
    p = os.path.join(ROOT, 'download.html'); d = open(p, encoding='utf-8').read()
    d = re.sub(r'버전 [\d.]+ · [\d.]+MB', f'버전 {ver} · {size}', d); open(p, 'w', encoding='utf-8').write(d)
    print('준비 완료:', info)
