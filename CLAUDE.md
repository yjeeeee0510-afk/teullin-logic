# 틀린로직맞추기 — 작업 안내 (Claude Code용)

틀린그림 찾기 → 네모네모 로직 → 퍼즐 맞추기가 번갈아 나오는 510라운드 모바일 웹 퍼즐 게임.
사용자는 한국어로 대화하고, 화면 문구도 모두 한국어로 쓴다. 휴대폰(안드로이드·아이폰) 화면이 기준.

## 배포
- GitHub Pages: `main` 브랜치 루트가 그대로 https://yjeeeee0510-afk.github.io/teullin-logic/ 에 올라간다 (`.nojekyll`).
- 고치면 `sw.js`의 `CACHE` 버전 숫자를 하나 올린다 (예: `sekan-v22` → `sekan-v23`). 안 올리면 홈 화면 앱에 예전 화면이 남는다.
- 그림 파일을 추가·삭제하면 `sw.js`의 `CORE` 목록도 맞춘다.
- 파일 하나짜리 HTML이 필요하면 `python3 tools/build_single.py` → `dist/틀린로직맞추기.html` (그림·랭킹 설정을 안에 넣음).

## 패치 번호 (사용자 요청, 꼭 지킬 것)
- 시작 화면 우측 하단에 흰 작은 글씨로 `패치 X.Y` (`index.html`의 `#introVer`).
- 플레이어에게 보이는 변경을 올릴 때마다 0.1씩 올리고(1.7 → 1.8 → 1.9 → 2.0 …), 아래 기록에 한 줄 추가하고, `index.html`의 `PATCH_NOTES` 맨 위에도 [번호, 날짜, 제목, 바뀐 점들]을 넣는다(운영진 설정 → 패치 노트에 보임). 글자 수정·내부 도구처럼 안 보이는 변경은 올리지 않는다.
- 기록: 1.0 웹 공개 · 1.1 휴대폰 한 화면 인게임 · 1.2 난이도 4단계·360라운드 · 1.3 프로필·십이지 사진·운영진 · 1.4 지역 그림·인게임 배경 · 1.5 섬 지도·배 이동·조약돌·선착장 · 1.6 누끼·그림자·이동 장면·바닷가 그림 · 1.7 로직 720문제(겹침 없음) · 1.8 시작 화면 '게임시작' 깜박이는 흰 글씨 · 1.9 게임 켜면 진행 중인 라운드로 바로 · 2.0 힌트 최대 10개·30분마다 1개 · 2.1 하트(최대 10·10분마다 1)·실패(실수 5번) · 2.2 하늘섬(361~510)·날아오르는 이동·지역 별 80%·틀린그림 새 차이·거울 라운드 · 2.3 지도에 다른 플레이어 프로필 · 2.4 별점별 클리어 코인(25·50·100, 차액만) · 2.5 업적·칭호 · 2.6 시작 화면 패치 연한 회색·'Made by 중독 게임사' · 2.7 효과음(상황별 20가지, 설정에서 끄기) · 2.8 지역 이동 별 70% · 2.9 배 이동 소리 파도 가르기 · 3.0 클리어 창 재도전·프로필 테두리 12가지·랭킹 이름 변경 없앰 · 3.1 과자 나라(300라운드·쿠키 하트·오늘의 과자·과자 나라 순위·본 게임 연동) · 3.2 과자 나라 클리어 창 재도전 · 3.3 이미 깬 라운드 다시 하기는 하트(과자 나라 쿠키) 1개 씀 · 3.4 틀린그림·퍼즐 그림 지역 섞기(배경 지역 + 다른 지역 2곳, 낮 배경엔 밤 물건 제외) · 3.5 과자 판 점 크게·칸 색 연하게 · 3.6 과자 나라 전체 두 단계 이상 어렵게(6×6~10×10, 오늘의 과자 7~10) · 3.7 라운드 십이지 작게·내 차례 라운드에 내 프로필 '나' 핀 · 3.8 로직 다 풀면 그림 색·퍼즐 1:1 직소 조각 모양

## 파일
- `index.html` — 게임 전체 (HTML·CSS·JS 한 파일). 512줄·976줄 근처는 base64 그림이 들어 있는 아주 긴 줄이라 통째로 읽지 말 것.
- `rank-config.js` — Supabase 주소와 공개(publishable) 키. secret/service_role 키는 절대 넣지 않는다.
- `img/scenes/*.png` 배경(800×600), `img/sprites/*.png` 물건 그림, `img/bg/zone*.jpg` 인게임 지역 배경 사진(사용자가 준 그림).
- `tools/art/` — 지역 그림을 직접 그린 SVG 원본(`art.cjs`)과 PNG로 뽑는 스크립트(`render.cjs`, playwright 필요).
- `supabase/changes.sql` — 지금까지 서버에 실행한 SQL 기록.
- `tools/ai_art/` — OpenAI 이미지 API로 게임 그림 90장(배경 4·물건·하늘 장식)을 새로 만드는 도구.
- `tools/matting/candy.py` — 과자 나라 그림(파란 바탕 #0047FF 물건 모음 7장, 흰 바탕 과자 칸, 지도·입구·배경) 누끼 → `img/candy/`. 물건 사이에 갇힌 그늘진 파란 바탕까지 지움.
- `tools/candy/gen.py` — 과자 나라 문제집(300라운드 + 매일 퍼즐 크기별 30개) → `index.html`의 `/*CANDY_BANK*/` 블록. 모두 추론만으로 풀림(답 하나). 10분쯤 걸림.
- `tools/candy/ranking.sql` — 과자 나라 순위용 SQL(칸 candy_round·candy_stars·candy_time, 함수 leaderboard_candy_top/me). 2026-10-30 실행 완료(`supabase/changes.sql`에 기록).
- `tools/matting/sky.py` — 하늘섬 그림(흰 바탕 물건·하늘섬, 초록 바탕 구름, 투명 배) 누끼.
- `tools/matting/` — 물건 모음 사진에서 누끼를 따는 도구와 12가지 바탕 검수표(`qa.py`). 물건 그림은 `img/sprites/*.webp`(목록 `SPR_WEBP`).

## OpenAI로 그림 바꾸기 (tools/ai_art)
- API 키는 사용자의 PC 환경 변수 `OPENAI_API_KEY`에만 둔다. 파일·저장소·게임 코드·대화에 키를 적지 않는다. 키를 대화창에 붙여 넣으려 하면 말린다.
- 모델은 `OPENAI_IMAGE_MODEL`(기본 `gpt-image-1`). 실행 전에 OpenAI 요금표와 모델 이름을 확인하고, 사용자에게 장수와 대략적인 요금을 알린 뒤 진행한다.
- 순서
  1. `node tools/ai_art/generate.mjs --dry --zone "꽃 언덕"` 으로 요청 목록 확인 (요금 없음)
  2. `node tools/ai_art/generate.mjs --zone "꽃 언덕"` → `tools/ai_art/out/raw/` (이미 만든 건 건너뜀, `--only 이름,이름`, `--force`, `--quality low|medium|high`)
  3. `python3 tools/ai_art/process.py` → 크기 맞춰 `img/` 에 넣고 `sw.js` 캐시 버전을 올림, 원래 그림은 `out/backup/`
  4. `tools/ai_art/out/preview.png`와 휴대폰 크기 게임 화면을 찍어 사용자에게 보여 주고, 좋다고 하면 커밋·푸시
- 그림 목록·요청 문장은 `tools/ai_art/items.json` (지역 `zone`: 꽃 언덕·푸른 바다·눈 덮인 산·별빛 하늘·하늘). 색 변형(`variantOf`)은 바탕 그림을 편집해서 모양을 맞춘다.
- 이름은 `index.html`의 `REGION_THEMES`·`GROUPS`·`ART_H` 이름과 같아야 게임에 쓰인다. 새 물건을 추가하면 그 세 곳에도 넣는다.
- 그림이 바뀌면 `ART_FLIP`(좌우가 다른 그림)·`ART_NOCOLOR`(흰색이라 색 바꾸기가 티 안 나는 그림)도 새 그림 보고 다시 맞춘다.

## 게임 구조 (index.html 안)
- 라운드: `ZSTART=[0,90,180,270,360,510]`(지역 z는 `zLo(z)`~`zHi(z)`, 하늘섬만 150라운드), `MAXR=510`, `TSIZE=30`(단계 안 세부 난이도). `zoneOf(n)`, `isZoneEnd(n)`. `typeOf(n)=(n-1)%3` → 0 틀린그림, 1 로직, 2 퍼즐.
- 난이도 표 `ZONE_DIFF` (30라운드마다 한 줄): 틀린 곳 개수·로직 칸·퍼즐 조각·틀린 곳 미묘함(dd).
- 지역 `ZONES`: 꽃 언덕(아주 쉬움) → 푸른 바다(쉬움) → 눈 덮인 산(보통) → 별빛 하늘(어려움) → 하늘섬(아주 어려움). 지도는 라운드당 80px(`MAP.STEP`), 지역마다 섬 하나.
- 지도는 한 번에 한 지역(`VIEWZ`, localStorage `sekan-viewz`)만 보인다. 게임을 켤 때(`enterGame`)는 진행 중인 라운드(`P.unlocked`)의 지역으로 맞춘다. 땅은 화면 너비를 꽉 채우고(`landHTML`), 위쪽 끝 바다에 다음 지역 선착장(`#dockUp`), 아래쪽 끝(2지역부터)에 앞 지역으로 돌아가는 선착장(`#dockDown`).
- 위쪽 선착장은 그 지역 마지막 라운드를 깨고 그 지역 별을 70%(`ZONE_STAR_RATE`, `zoneNeed`) 모으면 열리고(이미 `P.revealed`로 연 지역은 그대로), 누르면 `travel(from,to)` → 배 장면(`playVoyage`) → 다음 지역 지도. 처음 가는 지역이면 `P.revealed`를 올리고 '○○ 오픈!'. 90·180·270라운드를 깬 직후 클리어 창의 버튼은 '선착장으로 가기'.
- 지역 끝 바닷가 그림 `SHORE_TOP` (`img/map/shore0~4.jpg`, 사용자 그림): 위쪽 끝은 그대로(`.shore-top`), 아래쪽 끝은 위아래 뒤집어(`.shore-bot`).
- 섬 바닥은 `img/map/zone0~4.jpg`(사용자가 준 지역 그림, 위아래로 이어지게 다듬은 타일)를 섬 모양 마스크로 깐다(`groundHTML`).
- 길은 없고 조약돌(`pebblesHTML`, 지역별 `PEB_KIND`: 꽃 언덕 조약돌·푸른 바다 조개·눈 덮인 산 눈덩이·별빛 하늘 빛나는 버섯·하늘섬 구름 발판 `pebCloud*`): 깬 라운드에서 다음 라운드(섬 끝이면 선착장)까지 3~4개. 마지막으로 본 라운드는 localStorage `sekan-peb`, 새로 깬 구간은 하나씩 놓이는 모션.
- 지역 이동 장면 `playVoyage(from,to,done)`: `img/voyage/`(옆에서 본 바다 sea.jpg·섬 isl*·배 vyBoat*, 사용자 그림)로, 배가 왼쪽 섬→오른쪽 섬(좌우 뒤집음)으로. 지역 분위기는 곱하기 색(`TINT`). 문구는 '○○로 출발!' → '○○ 도착!' → 지도에서 '○○ 오픈!'.
- 별빛 하늘 ↔ 하늘섬은 `playFlight`: 세로로 긴 하늘(밤→새벽→낮)을 카메라가 올라가고, 날개 달린 배(`vyShip`+`vyWing` 날갯짓)가 별빛 하늘 섬에서 하늘섬(`islSky`)으로. 돌아갈 땐 같은 움직임을 거꾸로.
- 로직 다 풀면 칸에 그림 색(`logicWinFx`, 클리어 창은 `LOGIC_WIN_MS` 1.5초 뒤): 물건 그림은 `LOGIC_COLORS`(`/*LOGIC_COLORS*/` 블록, `python3 tools/logic/colors.py` — 문제집을 다시 만들면 이것도 다시 실행), 도형은 `LOGIC_SHAPE_COL`, 무늬는 무지개.
- 퍼즐: 장면을 `makeScene(seed,true)`로 가운데 600×600(`JIG_X`·`JIG_W`)에만 물건을 놓고 2배 해상도로 잘라 1:1. 조각은 직소 모양(`jigEdges` 볼록·오목, `jigPath` clip-path, `.jpw`·`.jpc`, 탭 크기 `JIG_TAB` .3), 두 조각을 눌러 바꾸는 방식은 그대로.
- 네모네모 로직: 문제집 `LOGIC_BANK`(`/*LOGIC_BANK*/` 블록, `python3 tools/logic/gen.py`로 다시 만듦). 크기(5·6·7·8·10·12)마다 120문제, 물건 그림 축소(이름은 `tools/logic/names.json`, 풀면 '○○ 완성!')·도형·대칭/비대칭 무늬. 모두 줄 추론만으로 풀림(답 하나), 회전·뒤집기 중복과 비슷한 문제 제외. `logicFor(round)`: 같은 크기 라운드끼리 다른 문제, 다시 하면(`plays`) 아직 안 쓴 문제.
- 틀린그림·퍼즐 장면: `makeScene`이 배경 + 물건을 판마다 무작위 배치. `mixTheme(seed)`가 라운드 지역과 상관없이 배경 지역 하나 + 다른 지역 2곳의 물건을 섞는다(`REGION_THEMES`만 씀, 예전 Kenney `THEMES`는 안 씀, 낮 배경엔 별빛 하늘 물건 제외).
  - 하늘섬 틀린그림(`SPOT_PLUS`): 361~ 살짝 이동(nudge)·하나 더 생김(add), 421~ 살짝 기울기(tilt)·배경 속 차이(`bgPatch`, 배경 조각을 옆 조각으로 덮음), 작은 물건 우선·차이 사이 거리 줄임. `isMirror(r)`: 481~ 틀린그림 9라운드마다 오른쪽 그림 좌우 반전.
  - 바꿔치기 문제는 `GROUPS`(같은 물건의 색 변형 묶음), 크기는 `ART_H`, 뒤집기 허용은 `ART_FLIP`, 색 바꾸기 제외는 `ART_NOCOLOR`.
- 인게임 화면: `body.game-mode` — 위 상태줄(`#ghud`), 우측 상단 메뉴(`#gmMenu`, 일시정지), 우측 하단 게임 버튼(`#gdock`). 지역 배경은 `setGameBg`.
- 하트: `HEART_MAX=10`, `HEART_EVERY` 10분, 상점 `HEART_PRICE=100`. `startRound`에서 1개를 걸고(`S.held`) `clearStage`에서 돌려줌 — 처음 깬 라운드만. 이미 깬 라운드(`P.rounds[n]` 있음)는 깨도 안 돌려줌(과자 나라 쿠키도 같음, 오늘의 과자 제외). 실수 `MISS_MAX=5`(틀린그림 오답 터치·로직 틀린 칸)면 `failStage`. 그만두기·처음부터 다시는 건 하트를 잃음. 실수 수는 `S.miss`로 저장(이어하기 해도 유지). 운영진은 하트를 안 씀.
- 클리어 코인 `STAR_COIN=[0,25,50,100]`(라운드 별점 기준). 라운드마다 코인 받은 별 수 `P.rounds[n].cs`를 두고 `STAR_COIN[새 별]-STAR_COIN[cs]`만 준다. `cs`가 없는 예전 기록은 `stars`만큼 받은 것으로 침. `CLEAR_COIN`(50)은 예전 소급 지급(`backpay`)에만 씀. 2.4 소급(`starBackpay`, 한 번만 `P.starpaid`): `cs` 없는 라운드마다 `STAR_COIN[stars]-plays×50`이 양수면 지급(빼지는 않음), 그 뒤 `cs=stars`.
- 업적 `ACH` (`LIST`: 진행·지역·별·칭호·끈기, 단계 `tiers`·보상 `rw`). 받은 단계는 `P.ach.got[id]`, 끈기 횟수 `P.ach.c.up/back`, 실패 표시 `P.ach.fail`. 지도 위쪽 메달 버튼(`#achBtn`, 받을 게 있으면 빨간 점). 칭호는 게임 종류별 별 3개 라운드 10·50·100·200 → 초보·중수·고수·달인(`P.title`, 업적 보상을 받아야 열림). 한 종류 라운드가 170개라 200(달인)은 `max`보다 커서 보이지만 비활성. 칭호는 `leaderboard.title`로 랭킹에 보냄(칸이 없으면 빼고 다시 보냄).
- 효과음 `SFX`(Web Audio로 직접 합성, 소리 파일 없음): `SFX.play(이름)` — tap·pebble·hit·combo·miss·hint·paint·line·pick·piece·clear·star·fail·coin·buy·empty·sail·fly·open·badge. 사용자가 고른 시안(A 실로폰 기본, 조약돌·실수·힌트·날갯짓은 B 말랑 버블, 실패·코인·배 출발은 C 8비트). 버튼 소리는 document click 캡처로 자동(게임판·`data-sfx="none"` 제외). 켜기/끄기는 설정 `#stSfx`, localStorage `sekan-sfx`.
- 과자 나라 `CANDY` (Meowdoku 방식, 스타배틀 1개): 지도 오른쪽 가운데 `#candyGo` → 과자 마을 지도(`CANDY.showMap`, 300라운드 한 지역, 라운드당 82px, 발판 마카롱·젤리빈, 구간 장식 사탕 숲 1~100·쿠키 언덕 101~200·초콜릿 성 201~300). 왼쪽 가운데 '돌아가기', 오른쪽 가운데 '오늘의 과자'. 판 크기 6(1~20)·7(21~90)·8(91~140)·9(141~240)·10(241~300), 뒤로 갈수록 어려운 기법 필요(191~240·271~300은 구역 묶어 보기), 별 3개 시간 기준 칸 수×3+30초. 한 번 누르면 ×, 한 번 더 누르면 친구(틀리면 실수, 5번이면 실패), 친구가 앉으면 못 쓰는 칸에 점 표시, ×는 그어서 여러 칸. 쿠키 하트는 본 게임 하트와 따로(`P.candy.hearts`, 최대 10·10분마다 1·100코인). 오늘의 과자: 요일마다 크기(일10·월화7·수목8·금토9), 쿠키 안 씀, 처음 50코인·7일 연속 200·한 달 완성 500과 왕관 도장. 기록 `P.candy`(unlocked·rounds·daily·months), `mergeP`에서 합침. 랭킹 탭 '과자 나라'는 서버 함수가 없으면 '준비 중'. 본 게임과 연동: 구간 `PART`는 본 게임 `P.revealed`에 따라 열림(사탕 숲 처음부터·쿠키 언덕 푸른 바다·초콜릿 성 눈 덮인 산, `capTo`), 잠긴 구간 앞 안내판 `.cm-lock`, 본 게임에서 지역을 열 때 '과자 나라 ○○도 열렸어요!'. 업적 `ACH`에 '과자' 탭(candyClear·candyDaily)과 칭호 candyStar(과자 초보~달인), 과자 마을 지도에도 업적 버튼. 과자 나라 화면에서는 `CANDY.isOn()`이라 `showMenu`가 과자 마을을 그림(게임을 켜면 본 지도).
- 진행 기록 `P` (localStorage `sekan-progress`), 아이디 계정이면 Supabase `progress` 표와 동기화(`mergeP`).
- 프로필 테두리 `FRAMES`(업적 `ACH.gotOf(id)` 단계로 열림, 운영진은 모두): `P.frame`·`P.frameAt`, 클래스 `fr fr-<id>`를 `.pf-av`·`.pf-big`에. 프로필 → 테두리 고르기(`openFrames`). 랭킹 서버에는 안 보냄.
- 지도 라운드 십이지는 60px(지금 라운드 70px), 지금 라운드 위에 내 프로필 핀 `mePin()`(`.me-pin`, 본 게임·과자 마을 지도 둘 다).
- 클리어 창 `#mRetry`(재도전, `retryRound`) → `startRound` (하트 1개 다시 걺).
- 프로필: 좌측 상단 `#profBtn`, 십이지 친구 얼굴 선택(`P.avatar`), 이름은 `ZODIAC.NAMES`(찍찍이·음메·어흥이·깡총이·미르·스르르·다그닥·몽실이·끼끼·꼬꼬·멍멍이·꿀꿀이).
- 지도 위 다른 플레이어(`OTHERS`): 서버 함수 `leaderboard_players`(랭킹에 기록이 있는 모든 사람, 게스트 포함·접속 여부 상관없음)로 받아 `best_round+1` 라운드 옆에 얼굴(최대 3개+N)과 닉네임, 누르면 그 라운드 목록. 1분 캐시, 함수가 없으면 아무것도 안 보임. 내 기록은 빼고 보임.
- 접속 신호: 세션이 이미 있는 사람만 45초마다 `presence` 표에 upsert(`RANK.beat`), 화면을 숨기거나 닫으면 online=false. 운영진 설정 → '접속 중인 사람'(`openOnline`)이 서버 함수 `presence_online()`(운영진 이메일만, 90초 안 신호)으로 10초마다 목록을 받음. 표·함수가 없으면 조용히 멈춤.
- 운영진: `ADMIN_IDS`(`yjeeeee0510`, `dhsb1234`) — 랭킹 제외, 모든 라운드 열림, 설정 → 운영진 도구(모든 화면 보기), 일시정지 메뉴의 바로 클리어.

## 랭킹 서버 (Supabase, 프로젝트 teullin-logic)
- 표: `leaderboard`(닉네임·최고 라운드·별·점수·클리어 횟수·평균 시간·avatar·title), `progress`(아이디별 진행 기록 JSON).
- 표 `presence`(id·nickname·avatar·online·since·last_seen, 시간은 트리거 `presence_touch`가 서버 시간으로). 함수 `presence_online()`.
- 함수: `leaderboard_top(n)`, `leaderboard_me()`, `leaderboard_players(n)`(지도용, 게스트 포함 모두), `leaderboard_candy_top(n)`·`leaderboard_candy_me()`(과자 나라 순위), `delete_my_account()`. 운영진 기록은 트리거 `leaderboard_skip_admin`이 막는다 (운영진 이메일 목록, 클라이언트 `ADMIN_IDS`와 맞출 것).
- 아이디 로그인은 `아이디@teullin.game` 이메일 형식으로 Supabase Auth에 저장된다.
- 운영 데이터베이스 변경(SQL)은 사용자가 Supabase SQL Editor에서 직접 실행한다. SQL을 만들어 주고, 실행 전에도 게임이 깨지지 않게 클라이언트에 대비 코드를 둔다.
- 실행할 SQL이 생기면 항상 브라우저에서 SQL Editor를 SQL이 채워진 채로 열어 준다 (사용자 요청): `https://supabase.com/dashboard/project/mceiajddsvxlunsovoth/sql/new?content=<URL 인코딩한 SQL>`. Run은 사용자가 누른다.

## 확인 방법
- `python3 -m http.server 8765` 로 띄우고 playwright로 휴대폰 크기(390×844, 360×640) 화면을 찍어 본다.
- 스크립트는 즉시실행 함수 안에 있어서 페이지에서 `startRound` 같은 함수를 직접 부를 수 없다. 지도 버튼(`.nd[data-r="N"]`) → `#rsGo` 클릭으로 들어간다.
- 커밋 작성자: `yjeeeee0510-afk <yjeeeee0510@gmail.com>`.
