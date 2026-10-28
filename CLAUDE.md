# 틀린로직맞추기 — 작업 안내 (Claude Code용)

틀린그림 찾기 → 네모네모 로직 → 퍼즐 맞추기가 번갈아 나오는 360라운드 모바일 웹 퍼즐 게임.
사용자는 한국어로 대화하고, 화면 문구도 모두 한국어로 쓴다. 휴대폰(안드로이드·아이폰) 화면이 기준.

## 배포
- GitHub Pages: `main` 브랜치 루트가 그대로 https://yjeeeee0510-afk.github.io/teullin-logic/ 에 올라간다 (`.nojekyll`).
- 고치면 `sw.js`의 `CACHE` 버전 숫자를 하나 올린다 (예: `sekan-v22` → `sekan-v23`). 안 올리면 홈 화면 앱에 예전 화면이 남는다.
- 그림 파일을 추가·삭제하면 `sw.js`의 `CORE` 목록도 맞춘다.
- 파일 하나짜리 HTML이 필요하면 `python3 tools/build_single.py` → `dist/틀린로직맞추기.html` (그림·랭킹 설정을 안에 넣음).

## 파일
- `index.html` — 게임 전체 (HTML·CSS·JS 한 파일). 512줄·976줄 근처는 base64 그림이 들어 있는 아주 긴 줄이라 통째로 읽지 말 것.
- `rank-config.js` — Supabase 주소와 공개(publishable) 키. secret/service_role 키는 절대 넣지 않는다.
- `img/scenes/*.png` 배경(800×600), `img/sprites/*.png` 물건 그림, `img/bg/zone*.jpg` 인게임 지역 배경 사진(사용자가 준 그림).
- `tools/art/` — 지역 그림을 직접 그린 SVG 원본(`art.cjs`)과 PNG로 뽑는 스크립트(`render.cjs`, playwright 필요).
- `supabase/changes.sql` — 지금까지 서버에 실행한 SQL 기록.

## 게임 구조 (index.html 안)
- 라운드: `MAXR=360`, `ZSIZE=90`(난이도 단계·지역), `TSIZE=30`(단계 안 세부 난이도). `typeOf(n)=(n-1)%3` → 0 틀린그림, 1 로직, 2 퍼즐.
- 난이도 표 `ZONE_DIFF` (30라운드마다 한 줄): 틀린 곳 개수·로직 칸·퍼즐 조각·틀린 곳 미묘함(dd).
- 지역 `ZONES`: 꽃 언덕(아주 쉬움) → 푸른 바다(쉬움) → 눈 덮인 산(보통) → 별빛 하늘(어려움). 지도는 라운드당 80px, 지역당 7,200px.
- 틀린그림·퍼즐 장면: `makeScene`이 배경 + 물건(`THEMES`/`REGION_THEMES`)을 판마다 무작위 배치. `themeFor(round)`가 지역 테마를 고른다.
  - 바꿔치기 문제는 `GROUPS`(같은 물건의 색 변형 묶음), 크기는 `ART_H`, 뒤집기 허용은 `ART_FLIP`, 색 바꾸기 제외는 `ART_NOCOLOR`.
- 인게임 화면: `body.game-mode` — 위 상태줄(`#ghud`), 우측 상단 메뉴(`#gmMenu`, 일시정지), 우측 하단 게임 버튼(`#gdock`). 지역 배경은 `setGameBg`.
- 진행 기록 `P` (localStorage `sekan-progress`), 아이디 계정이면 Supabase `progress` 표와 동기화(`mergeP`).
- 프로필: 좌측 상단 `#profBtn`, 십이지 친구 얼굴 선택(`P.avatar`), 이름은 `ZODIAC.NAMES`(찍찍이·음메·어흥이·깡총이·미르·스르르·다그닥·몽실이·끼끼·꼬꼬·멍멍이·꿀꿀이).
- 운영진: `ADMIN_ID='yjeeeee0510'` — 랭킹 제외, 모든 라운드 열림, 설정 → 운영진 도구(모든 화면 보기), 일시정지 메뉴의 바로 클리어.

## 랭킹 서버 (Supabase, 프로젝트 teullin-logic)
- 표: `leaderboard`(닉네임·최고 라운드·별·점수·클리어 횟수·평균 시간·avatar), `progress`(아이디별 진행 기록 JSON).
- 함수: `leaderboard_top(n)`, `leaderboard_me()`, `delete_my_account()`. 운영진 기록은 트리거 `leaderboard_skip_admin`이 막는다.
- 아이디 로그인은 `아이디@teullin.game` 이메일 형식으로 Supabase Auth에 저장된다.
- 운영 데이터베이스 변경(SQL)은 사용자가 Supabase SQL Editor에서 직접 실행한다. SQL을 만들어 주고, 실행 전에도 게임이 깨지지 않게 클라이언트에 대비 코드를 둔다.

## 확인 방법
- `python3 -m http.server 8765` 로 띄우고 playwright로 휴대폰 크기(390×844, 360×640) 화면을 찍어 본다.
- 스크립트는 즉시실행 함수 안에 있어서 페이지에서 `startRound` 같은 함수를 직접 부를 수 없다. 지도 버튼(`.nd[data-r="N"]`) → `#rsGo` 클릭으로 들어간다.
- 커밋 작성자: `yjeeeee0510-afk <yjeeeee0510@gmail.com>`.
