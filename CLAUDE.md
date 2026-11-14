# 틀린로직맞추기 — 작업 안내 (Claude Code용)

틀린그림 찾기 → 네모네모 로직 → 퍼즐 맞추기가 번갈아 나오는 720라운드 모바일 웹 퍼즐 게임.
사용자는 한국어로 대화하고, 화면 문구도 모두 한국어로 쓴다. 휴대폰(안드로이드·아이폰) 화면이 기준.

## 사용자와 일하는 방식 (사용자 요청)
- 설명은 간단 명료하게, 결론부터(두괄식).
- 물어볼 게 여러 개여도 한 번에 묶어서 묻고, 한 번에 정확한 결과를 내도록 한다.
- 사용자는 엔지니어지만 이 게임 코드는 Claude가 맡아 짠다. 저장소 커밋·푸시(배포)까지 Claude가 한다.
- 화면이 바뀌는 작업은 휴대폰 크기 화면을 찍어 보여 주고 진행한다.
- 작업하다 새로 만든 파일(문서·zip·AAB·시안 등 사용자가 보관할 결과물)은 구글 드라이브 `틀린로직맞추기` 폴더(폴더 ID `1iwUG8Q5u6mQk9O1_cA9caBxus7besIHR`)에도 넣는다(사용자 요청 2026-11-14). 드라이브 도구는 한 번에 10MB까지만 올라가서, 큰 파일(AAB·그림 원본 zip)은 올리지 못하면 사용자에게 파일을 직접 보내고 그 사실을 알린다. 서명 키·비밀번호는 이 폴더 규칙에 포함하지 않는다(키는 `앱서명키_보관용.zip`에 따로 보관 중이고 새로 올리거나 복사하지 않는다).


## 회의 모드·인수인계 (사용자 요청)
- 사용자가 "회의모드"라고 하면 코드는 고치지 않고 안건을 하나씩 정하며 논의한다. 규칙·안건·결정사항·구글 플레이 출시 현황은 `docs/MEETING.md`에 있다. 새 세션은 이 파일을 먼저 읽고, 결정이 날 때마다 그 파일을 고쳐 둔다.

## 방향
- 제작사 이름 '중독 게임사'(시작 화면 'Made by 중독 게임사').
- 웹(GitHub Pages)으로 안드로이드·아이폰·브라우저 모두 지원, 나중에 플레이스토어용 안드로이드 앱으로 출시 예정.
- 그림은 저작권 걱정 없는 것만 쓴다. 사용자가 ChatGPT로 만들어 보내는 그림이 기본(원본은 `art-src/`).
- 운영진 아이디는 `yjeeeee0510`, `dhsb1234`.
- 예전 기획 문서(claude.ai 프로젝트 '게임제작'): 하늘섬(패치 2.2)·과자 나라(패치 3.1) — 둘 다 반영 완료, 내용은 아래 '게임 구조'에 들어 있음.

## 배포
- 안드로이드 앱(5.6~): `app/`(Capacitor 8, 앱 아이디 `com.jungdok.teullinlogic`, 이름 '틀린로직맞추기'). 순서: `cd app && node copy-web.mjs && npx cap sync android && cd android && ./gradlew assembleRelease bundleRelease` (ANDROID_HOME 필요, npm은 프록시 옵션 필요) → `app/android/app/build/outputs/apk/release/app-release.apk`를 `download/teullinlogic.apk`로 복사해 커밋. 다운로드 안내 `download.html`(버전·용량 글자도 고침). 앱 버전 = 패치 번호(versionName 5.6, versionCode 56, `app/build.gradle`이 index.html에서 읽음) → 게임을 고친 뒤 앱도 새로 만들어 올린다.
- 앱 업데이트(5.8~): 앱은 켤 때 `version.json`(저장소 루트)의 `code`가 자기 versionCode보다 크면 '새 버전이 나왔어요' 안내(`UPD`) → '받기'는 네이티브 플러그인 `ApkUpdate`(`app/android/.../ApkUpdatePlugin.java`, 권한 REQUEST_INSTALL_PACKAGES)가 APK를 받아 설치 화면을 연다. 새 앱 올리기는 `python3 tools/app/release.py`(빌드·APK 복사·version.json·download.html 글자) → 커밋·푸시. 플레이스토어 판을 만들 땐 REQUEST_INSTALL_PACKAGES 권한과 안내를 빼야 한다.
- 서명 키는 저장소에 없다: `app/android/keystore.properties`(storeFile·storePassword·keyAlias=teullinlogic·keyPassword, .gitignore)와 키 파일 `teullinlogic-release.keystore`는 사용자가 보관(같은 키가 없으면 업데이트 설치 불가). 새 세션에서 빌드하려면 사용자에게 키 파일과 비밀번호를 받아야 한다.
- 앱 아이콘·시작 화면: `python3 tools/app/make_res.py`(원본 `art-src/app/icon.png`·`icon_fg.png`·`icon_bg.png`·`splash.png`, 없으면 icons/icon-512.png).
- 앱 안에서는 서비스 워커를 쓰지 않는다(파일이 앱에 들어 있음). 안드로이드 화면 막대 여백은 Capacitor가 넣는 `--safe-area-inset-*`를 `max(env(...),var(...))`로 함께 쓴다. 뒤로 버튼은 `NATIVE`(App 플러그인) → `__sekanBack`.
- GitHub Pages: `main` 브랜치 루트가 그대로 https://yjeeeee0510-afk.github.io/teullin-logic/ 에 올라간다 (`.nojekyll`).
- 고치면 `sw.js`의 `CACHE` 버전 숫자를 하나 올린다 (예: `sekan-v22` → `sekan-v23`). 안 올리면 홈 화면 앱에 예전 화면이 남는다.
- 그림 파일을 추가·삭제하면 `sw.js`의 `CORE` 목록도 맞춘다.
- **그림 내용을 바꾸면(같은 파일 이름) `index.html`의 `ASSET_V`와 `sw.js`의 `AV`를 같이 올린다.** 모든 `img/` 주소에 `?v=`가 붙어(`embedded()`), 안 올리면 휴대폰에 남은 예전 그림이 계속 보인다.
- 파일 하나짜리 HTML이 필요하면 `python3 tools/build_single.py` → `dist/틀린로직맞추기.html` (그림·랭킹 설정을 안에 넣음).

## 패치 번호 (사용자 요청, 꼭 지킬 것)
- 시작 화면 우측 하단에 흰 작은 글씨로 `패치 X.Y` (`index.html`의 `#introVer`).
- 플레이어에게 보이는 변경을 올릴 때마다 0.1씩 올리고(1.7 → 1.8 → 1.9 → 2.0 …), 아래 기록에 한 줄 추가하고, `index.html`의 `PATCH_NOTES` 맨 위에도 [번호, 날짜, 제목, 바뀐 점들]을 넣는다(운영진 설정 → 패치 노트에 보임). 글자 수정·내부 도구처럼 안 보이는 변경은 올리지 않는다.
- 기록: 1.0 웹 공개 · 1.1 휴대폰 한 화면 인게임 · 1.2 난이도 4단계·360라운드 · 1.3 프로필·십이지 사진·운영진 · 1.4 지역 그림·인게임 배경 · 1.5 섬 지도·배 이동·조약돌·선착장 · 1.6 누끼·그림자·이동 장면·바닷가 그림 · 1.7 로직 720문제(겹침 없음) · 1.8 시작 화면 '게임시작' 깜박이는 흰 글씨 · 1.9 게임 켜면 진행 중인 라운드로 바로 · 2.0 힌트 최대 10개·30분마다 1개 · 2.1 하트(최대 10·10분마다 1)·실패(실수 5번) · 2.2 하늘섬(361~510)·날아오르는 이동·지역 별 80%·틀린그림 새 차이·거울 라운드 · 2.3 지도에 다른 플레이어 프로필 · 2.4 별점별 클리어 코인(25·50·100, 차액만) · 2.5 업적·칭호 · 2.6 시작 화면 패치 연한 회색·'Made by 중독 게임사' · 2.7 효과음(상황별 20가지, 설정에서 끄기) · 2.8 지역 이동 별 70% · 2.9 배 이동 소리 파도 가르기 · 3.0 클리어 창 재도전·프로필 테두리 12가지·랭킹 이름 변경 없앰 · 3.1 과자 나라(300라운드·쿠키 하트·오늘의 과자·과자 나라 순위·본 게임 연동) · 3.2 과자 나라 클리어 창 재도전 · 3.3 이미 깬 라운드 다시 하기는 하트(과자 나라 쿠키) 1개 씀 · 3.4 틀린그림·퍼즐 그림 지역 섞기(배경 지역 + 다른 지역 2곳, 낮 배경엔 밤 물건 제외) · 3.5 과자 판 점 크게·칸 색 연하게 · 3.6 과자 나라 전체 두 단계 이상 어렵게(6×6~10×10, 오늘의 과자 7~10) · 3.7 라운드 십이지 작게·내 차례 라운드에 내 프로필 '나' 핀 · 3.8 로직 다 풀면 그림 색·퍼즐 1:1 직소 조각 모양 · 3.9 아이디 바꿔 로그인할 때 기록 섞임 고침 · 4.0 틀린그림 '원본'·'다른 그림' 글씨를 그림 바깥 위로 · 4.1 퍼즐 조각 다시 네모로 · 4.2 그림 전체 새로(물건 182·배경 24·화면 아이콘 15, 예전 Kenney 그림 삭제) · 4.3 그림 주소에 버전(?v=) 붙여 예전 그림 캐시 안 쓰게 · 4.4 쿠키 없을 때 멈춤·날개 위치·로직 숫자 진하게·칠할 때 색·무늬 이름 · 4.5 하늘섬 배 앞쪽 작은 날개 없앰 · 4.6 하늘섬 391~480 퍼즐 7×7 · 4.7 하늘섬 481~510 퍼즐 8×8 · 4.8 로직 그림 겹침 없앰(그림 이름 문제집 전체에서 한 번만·12×12 560문제) · 4.9 천국(511~720)·천마 마차 이동·지역별 선착장·지도 배를 이동 배 모양으로 · 5.0 QA 반영(이어하기 시간·진행 유지, 메뉴 효과 숨김, 로직·틀린그림 확대, 힌트·조각 표시, 지역 이동 목록) · 5.1 천마 끈과 마차 끌채 붙임 · 5.2 천마+마차 한 장(pegCoach)·날개 등에서 뒤로 · 5.3 천마 날갯짓 되살림 · 5.4 틀린그림 부분 색 변화·단계별 차이 비율·거울=도전 라운드(지역마다·⇄·보너스 50·차이 1~2개 적게·첫 설명) · 5.5 효과음 파일 40개(대표 선택: 클로드·지팀장 시안)·새 소리 14개 연결 · 5.6 안드로이드 앱(APK)·다운로드 페이지·뒤로 버튼·안드로이드 화면 막대 여백 · 5.7 앱 아이콘·시작 화면(어흥이, `art-src/app/`) · 5.8 앱 자동 업데이트 안내·앱 안에서 받아 설치 · 5.9 운영진 비밀번호 재설정 도구(서버 함수 admin_set_password) · 6.0 로직 풀 땐 검은색·클리어하면 그림 색·확대 돋보기 버튼 없앰 · 6.1 다크 모드에서도 로직판 흰 배경+검은 칸 고정 · 6.2 십이지 친구 새 그림(얼굴·몸, `art-src/new/Z1~Z4`, `tools/matting/apply_zodiac.py`) · 6.3 인게임 상단 새 모습(라운드·점수·시간+목숨 하트 `#ghLives`·`renderLives`)·과자 나라 숨은 친구 줄(`#cdFriends`·`G.seatOrder`)·로직 두 손가락 확대 없앰·시작 배경 새 그림 · 6.4 업데이트 안내를 시작 화면에서(`UPD.show`에 `.updsheet` z-index 70, `auto`는 intro 대기 안 함)·안내에서 패치 내용 숨김 · 6.5 틀린그림 라벨 제거·그림 키움(figcaption 없앰, fitBoard CAP=0)·판 상단 정렬(#board flex-start, 스팟은 :has(.pics) 가운데)·로직 줄완성 글자 판 위 하나만(`.pop.lcomp`)·숨은 친구 슬롯 겹침 수정(`pop`→`cdpop`, 전역 `.pop`과 충돌)·과자 안내 처음 3번만(`sekan-cdhow`) · 6.6 프로필 카드(큰 캐릭터·정보 칸 5)·꾸미기(배경·받침·이름표·효과·동작·동행 친구 코인, 테두리·칭호·대표 배지 업적)·남의 프로필 카드·하트/힌트/쿠키 최대 5·별 코인 10/20/40·실수 방패·퍼즐 회전 라운드/고정/7×7 상한·지역 이동 배 개선·과자 나라 600라운드(11×11·12×12) · 6.7 지팀장 새 그림 대량 교체(이동 배·파도 띠·뱃머리 물보라·물방울, 받침 9·배경 9 그림, 동행 66쌍, 배지 16, 과자 칸 2; 소품은 어색해 뺌)

## 파일
- `art-src/` — 사용자가 준 그림 원본 보관(지역별 폴더, 목록·용도는 `art-src/README.md`). **누끼·크기 조정은 항상 여기 원본에서 다시 한다.** 새 원본을 받으면 맞는 폴더에 도구가 찾는 이름으로 넣고 README 표를 고친다.
- `index.html` — 게임 전체 (HTML·CSS·JS 한 파일). 512줄·976줄 근처는 base64 그림이 들어 있는 아주 긴 줄이라 통째로 읽지 말 것.
- `rank-config.js` — Supabase 주소와 공개(publishable) 키. secret/service_role 키는 절대 넣지 않는다.
- `img/scenes/*.png` 배경(800×600), `img/sprites/*.png` 물건 그림, `img/bg/zone*.jpg` 인게임 지역 배경 사진(사용자가 준 그림).
- `tools/art/` — 지역 그림을 직접 그린 SVG 원본(`art.cjs`)과 PNG로 뽑는 스크립트(`render.cjs`, playwright 필요).
- `supabase/changes.sql` — 지금까지 서버에 실행한 SQL 기록.
- `tools/ai_art/` — OpenAI 이미지 API로 게임 그림 90장(배경 4·물건·하늘 장식)을 새로 만드는 도구.
- `tools/matting/candy.py` — 과자 나라 그림(파란 바탕 #0047FF 물건 모음 7장, 흰 바탕 과자 칸, 지도·입구·배경) 누끼 → `img/candy/`. 물건 사이에 갇힌 그늘진 파란 바탕까지 지움.
- `tools/candy/gen.py` — 과자 나라 문제집(300라운드 + 매일 퍼즐 크기별 30개) → `index.html`의 `/*CANDY_BANK*/` 블록. 모두 추론만으로 풀림(답 하나). 10분쯤 걸림.
- `tools/candy/gen_ext.py` — 과자 나라 301~600(11×11 150·12×12 150) 문제집(6.6). 구역·답을 36진수 한 글자(0-9a-z)로 적음(`decode`가 `parseInt(ch,36)`). `--apply`로 `/*CANDY_BANK*/`의 `r` 뒤에 붙임(1시간쯤, 4코어 병렬).
- `img/zbody/b0~11.webp`(큰 몸 그림 460×600, 프로필 카드용, 원본 `art-src/new/Z3·Z4`를 `tools/matting/chroma.py`로 높이 600에 맞춰 뽑음), `art-src/REQUEST-cosmetics.md`·`request-cosmetics.json` — 지팀장(사용자의 ChatGPT)에게 줄 꾸미기 그림 요청서(동행 쌍 66·소품·받침·카드 배경·배·물보라·배지·과자 칸 = 35번, 그림이 오면 `PAIRS_READY`·`BADGE_IMG` 등에 등록).
- **6.7 그림 교체**: 원본 `art-src/cos/`(V1 배·V2 물방울·V2C 물결 4·B1/B2 받침·BD1/BD2 배지·T1 과자 칸·P01~P17 동행 쌍·CB01~09 카드 배경, 요청서 `art-src/request-cosmetics.json`·`GPT-전달본.md`·`V2C-요청문.md`). 변환 `python3 tools/matting/build_cos.py`(누끼·크기·img/ 저장, T1 같은 흰 바탕은 바깥 윤곽만 따고 안쪽을 채움) → `img/voyage`(vyBoat*·waveBandA/B·bowSplash·dropsA/B)·`img/ped`·`img/badge`·`img/pair`(66쌍, `PAIRS_READY`는 `ANCH.pair` 키 전부)·`img/cosbg/bg_<id>.webp`(512×768)·`img/candy/tileLemon·tileSoda`. 지역 이동(`playVoyage`): 앞 파도 띠 `vy-front`·`vy-front2`는 waveBand 그림(좌우 거울로 이어 붙인 이음새 없는 띠, 아래쪽 마스크로 흐려짐)을 가로로 흘리고, 뱃머리 물보라 `vy-bow`·물방울 `vy-spray`(꼬리 물결 wakeTrail은 끊겨 보여서 뺌). 프로필 카드 `stageHTML`: 캐릭터는 `.pf-fig`(가로세로비 `ANCH`로 컨테이너 쿼리 크기, 동작 클래스는 fig에), 받침 그림은 `.pf-ped`(`PEDIMG`: 이름·비율·발 높이·너비%, 카드 높이가 작아도 받침 높이 34% 이하로 줄임), 배경 그림은 `center top/cover`. `tools/matting/anchors.py`는 머리 위치 표(소품용이었으나 소품을 뺌, 가로세로비만 씀).
- `tools/candy/ranking.sql` — 과자 나라 순위용 SQL(칸 candy_round·candy_stars·candy_time, 함수 leaderboard_candy_top/me). 2026-10-30 실행 완료(`supabase/changes.sql`에 기록).
- 새 그림(4.2): 원본 `art-src/new/<장>.png`(칸 순서는 `art-src/request.json`), 누끼 `python3 tools/matting/chroma.py <장들>` → `tools/matting/out/`(저장소 제외) → `python3 tools/matting/apply_new.py`로 `img/`에 넣음(배경 BG01~24 크기 맞춤, 지도 바닥 위아래 이음). 화면 아이콘은 `img/ui/ico*.webp`, 코드는 `UI(이름,클래스)`로 `<img class="uico">`(ICON·TYPE_ICON·TROPHY·GEAR·LOCK·STAR·STAR_P·메뉴 버튼). 별은 `st-on`/`st-off` 두 장을 `.on`/`.off`로 골라 보임.
- `tools/matting/sky.py` — 하늘섬 그림(흰 바탕 물건·하늘섬, 초록 바탕 구름, 투명 배) 누끼.
- `tools/matting/` — 물건 모음 사진에서 누끼를 따는 도구와 12가지 바탕 검수표(`qa.py`). 물건 그림은 `img/sprites/*.webp`(목록 `SPR_WEBP`).

## 누끼 품질 기준 (사용자 요청, 꼭 지킬 것)
- 누끼는 항상 '포토샵으로 손질한 것처럼' 깨끗하게. 기준을 하나라도 못 넘으면 게임에 넣지 않는다.
  1. 테두리: 흰 테·바탕색 테·뿌연 빛·계단 현상 없음. 경계는 1~2px 부드러운 안티에일리어싱.
  2. 색 오염 제거: 반투명 가장자리 픽셀에서 바탕색을 빼서 물건 원래 색으로 되살린다(포토샵 '색상 정화'와 같은 처리).
  3. 구멍 없음: 흰 눈·흰 몸통·구름 등 물건 안쪽은 꽉 찬 불투명. 진짜 뚫린 틈(울타리 사이 등)만 투명.
  4. 바닥 그림자·받침·회색 얼룩 없음. 물건에 붙은 눈·구름·물보라는 남김.
  5. 잘림·옆 물건 조각 없음, 여백은 둘레 몇 px만.
- 확인: 분홍(#ff2bd6)·진한 남색·흰색·지역 땅색 바탕에 올린 검수표를 만들어 직접 보고, 사용자에게 보여 준 뒤에 넣는다.
- 원본은 단색 바탕(초록 #00B140·파랑 #0047FF)이 가장 깨끗하다. 흰 바탕 원본에서 흰 물건은 흰색 경계를 특히 꼼꼼히 본다.

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
- 라운드: `ZSTART=[0,90,180,270,360,510,720]`(지역 z는 `zLo(z)`~`zHi(z)`, 하늘섬 150·천국 210라운드), `MAXR=720`, `TSIZE=30`(단계 안 세부 난이도). `zoneOf(n)`, `isZoneEnd(n)`. `typeOf(n)=(n-1)%3` → 0 틀린그림, 1 로직, 2 퍼즐.
- 난이도 표 `ZONE_DIFF` (30라운드마다 한 줄): 틀린 곳 개수·로직 칸·퍼즐 조각·틀린 곳 미묘함(dd).
- 지역 `ZONES`: 꽃 언덕(아주 쉬움) → 푸른 바다(쉬움) → 눈 덮인 산(보통) → 별빛 하늘(어려움) → 하늘섬(아주 어려움) → 천국(전설, 511~720). 지도는 라운드당 80px(`MAP.STEP`), 지역마다 섬 하나.
- 지도는 한 번에 한 지역(`VIEWZ`, localStorage `sekan-viewz`)만 보인다. 게임을 켤 때(`enterGame`)는 진행 중인 라운드(`P.unlocked`)의 지역으로 맞춘다. 땅은 화면 너비를 꽉 채우고(`landHTML`), 위쪽 끝 바다에 다음 지역 선착장(`#dockUp`), 아래쪽 끝(2지역부터)에 앞 지역으로 돌아가는 선착장(`#dockDown`).
- 위쪽 선착장은 그 지역 마지막 라운드를 깨고 그 지역 별을 70%(`ZONE_STAR_RATE`, `zoneNeed`) 모으면 열리고(이미 `P.revealed`로 연 지역은 그대로), 누르면 `travel(from,to)` → 배 장면(`playVoyage`) → 다음 지역 지도. 처음 가는 지역이면 `P.revealed`를 올리고 '○○ 오픈!'. 90·180·270라운드를 깬 직후 클리어 창의 버튼은 '선착장으로 가기'.
- 지역 끝 바닷가 그림 `SHORE_TOP` (`img/map/shore0~4.jpg`, 사용자 그림): 위쪽 끝은 그대로(`.shore-top`), 아래쪽 끝은 위아래 뒤집어(`.shore-bot`).
- 섬 바닥은 `img/map/zone0~4.jpg`(사용자가 준 지역 그림, 위아래로 이어지게 다듬은 타일)를 섬 모양 마스크로 깐다(`groundHTML`).
- 길은 없고 조약돌(`pebblesHTML`, 지역별 `PEB_KIND`: 꽃 언덕 조약돌·푸른 바다 조개·눈 덮인 산 눈덩이·별빛 하늘 빛나는 버섯·하늘섬 구름 발판 `pebCloud*`): 깬 라운드에서 다음 라운드(섬 끝이면 선착장)까지 3~4개. 마지막으로 본 라운드는 localStorage `sekan-peb`, 새로 깬 구간은 하나씩 놓이는 모션.
- 지역 이동 장면 `playVoyage(from,to,done)`: `img/voyage/`(옆에서 본 바다 sea.jpg·섬 isl*·배 vyBoat*, 사용자 그림)로, 배가 왼쪽 섬→오른쪽 섬(좌우 뒤집음)으로. 지역 분위기는 곱하기 색(`TINT`). 문구는 '○○로 출발!' → '○○ 도착!' → 지도에서 '○○ 오픈!'. 6.6: 배 흔들림을 `vy-heave`(위아래 2.3초)·`vy-pitch`(기울기 3.4초)로 나누고, 앞 파도 띠 `vy-front`·`vy-front2`(SVG, 배 아랫부분을 덮음)·수면 링 `vy-ring`·꼬리 물결 `vy-wake`·물보라 `vy-spray`. 배 그림에 물결이 같이 그려져 있어 물결 없는 배는 지팀장 요청(V1).
- 별빛 하늘 ↔ 하늘섬은 `playFlight`: 세로로 긴 하늘(밤→새벽→낮)을 카메라가 올라가고, 날개 달린 배(`vyShip`+뒤쪽 큰 날개 `vyWing` 하나 날갯짓, 앞쪽 작은 날개는 없음)가 별빛 하늘 섬에서 하늘섬(`islSky`)으로. 돌아갈 땐 같은 움직임을 거꾸로.
- 하늘섬 ↔ 천국은 `playHeaven`: 옆 하늘(`img/voyage/heavenSky.jpg`, 좌우 이음) 위로 천마 마차(`pegCoach`: pegBody 끈 끝과 carriage 끌채 끝을 맞춰 붙인 한 장, 날개 `pegWing`은 좌우 뒤집어 등 위에서 뒤쪽으로 날갯짓)가 왼쪽 섬→오른쪽 섬(`islSky`↔`islHeaven`), 구름(`flyCloud*`·`goldCloud*`) 앞뒤 두 겹이 흘러감.
- 천국: 그림 원본 `art-src/heaven/`(H1~H6·I3·BG25~29), 넣기 `python3 tools/matting/apply_heaven.py`. 틀린그림 12~14곳(`ZONE_DIFF`), 거울 라운드 511~ 6라운드마다(`isMirror`), 장면 물건 하나씩 더. 조약돌 `pebHeaven*`.
- 지도 선착장: `MAP_DOCK`(지역별 선착장)·`MAP_DECO`(물가 장식 A·B)·`MAP_BOATS`(이동 배를 위에서 본 그림 boatOrange·boatBlue·boatPurple·wingShip·pegCarriageTop, 지역 z에서 떠나는 배). 원본 `art-src/dock/`(B1·D1~D6).
- 로직 칸은 풀 때 검은색(`.cell.f`=var(--ink)), 다 풀면 `logicWinFx`가 그림 색을 입힘(`paintCell`은 색 안 칠함). 로직판(`.nono-wrap`)은 기기 다크 모드와 상관없이 색 변수(--card·--ink·--line·--soft·--hud-bg)를 밝게 고정해 늘 흰 배경+검은 칸(6.1). 이름 없는 무늬 문제는 `patternName`(대칭 모양으로 '나비 무늬' 등). 과자 판 칸 CSS는 `.cd-board .cc`로만(로직 세로 숫자도 `.cc`라 겹치면 안 됨).
- 로직 다 풀면 칸에 그림 색(`logicWinFx`, 클리어 창은 `LOGIC_WIN_MS` 1.5초 뒤): 물건 그림은 `LOGIC_COLORS`(`/*LOGIC_COLORS*/` 블록, `python3 tools/logic/colors.py` — 문제집을 다시 만들면 이것도 다시 실행), 도형은 `LOGIC_SHAPE_COL`, 무늬는 무지개.
- 퍼즐(6.6~): 크기 표 `ZONE_DIFF.jig` 3(1~90)·4(91~180)·5(181~360)·6(361~540)·7(541~720, 상한 7×7). 섞을 때 제자리 조각 0개, 제자리(회전 라운드는 방향도 맞아야)에 둔 조각은 고정(`.tile.ok`, 눌러도 선택 안 됨). 회전 라운드 `isRotate(r)`: 543부터 12라운드마다(543·555…711) — 모든 조각이 자리·방향 모두 틀려 시작, 고른 조각을 한 번 더 누르면 90도(`jig.rots` 누적, `S.jr` 저장), 처음 깨면 `CHAL_BONUS` 50, 지도 ⟳, 처음 만나면 설명 시트(`P.rotSeen`). `isChal=isMirror||isRotate`. 비슷한 조각이 많은 장면: `jigBias(r)` 361~540 50%·541~ 70%로 `PLAIN_BG`(beach·nightsky·skyisland) 배경(`mixTheme(seed,bias)`). 장면은 `makeScene(seed,true,bias)`로 가운데 600×600(`JIG_X`·`JIG_W`)에만 물건을 놓고 2배 해상도로 잘라 1:1. 조각은 네모 칸(`.tile`, 2px 틈, 4.1에서 직소 모양을 되돌림), 두 조각을 눌러 바꾸는 방식.
- 네모네모 로직: 문제집 `LOGIC_BANK`(`/*LOGIC_BANK*/` 블록, `python3 tools/logic/gen.py`로 다시 만듦). 크기(5·6·7·8·10·12)마다 120문제(12는 560), 물건 그림은 문제집 전체에서 한 번만(`SLOTS`·`PIC_QUOTA`), 물건 그림 축소(이름은 `tools/logic/names.json`, 풀면 '○○ 완성!')·도형·대칭/비대칭 무늬. 모두 줄 추론만으로 풀림(답 하나), 회전·뒤집기 중복과 비슷한 문제 제외. `logicFor(round)`: 같은 크기 라운드끼리 다른 문제, 다시 하면(`plays`) 아직 안 쓴 문제.
- 틀린그림·퍼즐 장면: `makeScene`이 배경 + 물건을 판마다 무작위 배치. `mixTheme(seed)`가 라운드 지역과 상관없이 배경 지역 하나 + 다른 지역 2곳의 물건을 섞는다(`REGION_THEMES`만 씀, 예전 Kenney 그림은 4.2에서 삭제, 낮 배경엔 별빛 하늘 물건 제외).
  - 하늘섬 틀린그림(`SPOT_PLUS`): 361~ 살짝 이동(nudge)·하나 더 생김(add), 421~ 살짝 기울기(tilt)·배경 속 차이(`bgPatch`, 배경 조각을 옆 조각으로 덮음), 작은 물건 우선·차이 사이 거리 줄임. `isMirror(r)`: 481~ 틀린그림 9라운드마다 오른쪽 그림 좌우 반전.
  - 차이 구성(5.4~): 지역별 비율 `RATIO`(꽃 언덕·푸른 바다 물건 변화5·부분1·미세0 / 눈 덮인 산·별빛 하늘 3·2·1 / 하늘섬·천국 2·3·1, 6곳 기준). 물건 변화=큰 물건 없어짐·바꿔치기·색(·하나 더), 부분 변화=`partSegs`(그림 속 같은 색 덩어리)를 `partTinted`로 그 부분만 색 회전(`o.part={k,deg}`) 또는 디테일 짝 그림(`DETAIL_READY`에 이름 넣으면 `<이름>X` 그림 사용, 원본 `art-src/detail/`, SPR_WEBP에도 추가), 미세=크기·뒤집기·이동·기울기·옅은 색·배경 조각.
  - 도전(거울) 라운드: `isMirror`(지역마다 `CHAL_SET` 3개쯤 + 481~ 9라운드마다 + 511~ 6라운드마다), `spotCount`로 틀린 곳 1~2개 적게, 지도 `.chal` ⇄ 표시, 처음 깨면 `CHAL_BONUS` 50코인, 처음 만나면 설명 시트(`P.mirrorSeen`). 테스트 모드에서 `window.__qa`(차이 목록·모두 표시).
  - 바꿔치기 문제는 `GROUPS`(같은 물건의 색 변형 묶음), 크기는 `ART_H`, 뒤집기 허용은 `ART_FLIP`, 색 바꾸기 제외는 `ART_NOCOLOR`.
- 이어하기: `snapRun()`이 1초마다·메뉴·화면 숨김 때 `S.el`(경과 ms)·`S.hu`(힌트)·`S.cp`(콤보 점수)·`S.found`(찾은 차이 번호)·`S.lg`/`S.lk`(로직 칸·틀린 칸)·`S.jo`/`S.jp`(조각 순서·원본 보기 낸 것)를 저장, `startStage`·`goTime`이 복원(이어하기는 '준비~' 없이 바로). 메뉴(#sheet)가 열리면 `.pop`·`.ready`·`#fx` 숨김.
- 로직 확대 `lgZoom`(`applyLogicZoom`·`zoomLogicTo`, 두 손가락 핀치만. 🔍 버튼은 6.0에서 없앰), 단서 `.cc`/`.rc` sticky, 누른 줄·칸 `.hl`(`logicFocus`). 터치는 110ms 기다렸다 칠함 → 그 사이 두 번째 손가락이면 칠하지 않음.
- 틀린그림 확대 `spot.vz`{z,cx,cy}(장면 좌표, 거울이면 오른쪽은 SW-cx), `sceneToCanvas`·`screenToScene`·`zoomSpot`·`bindSpotGestures`(탭=손 뗄 때 판정, 끌기=이동, 두 손가락=확대, `.press-dot`). 어려운 라운드는 `clearN`(약 40%) 뚜렷한 차이 먼저, 거울 라운드엔 `bgPatch` 없음.
- 지도 왼쪽 `#zoneGo` → `openZoneList`(가 본 지역 바로 가기).
- 인게임 화면: `body.game-mode` — 위 상태줄(`#ghud`), 우측 상단 메뉴(`#gmMenu`, 일시정지), 우측 하단 게임 버튼(`#gdock`). 지역 배경은 `setGameBg`.
- 하트(6.6~ 최대 5): `HEART_MAX=5`, `HEART_EVERY` 10분, 상점 `HEART_PRICE=100`. `startRound`에서 1개를 걸고(`S.held`) `clearStage`에서 돌려줌 — 처음 깬 라운드만. 이미 깬 라운드(`P.rounds[n]` 있음)는 깨도 안 돌려줌(과자 나라 쿠키도 같음, 오늘의 과자 제외). 실수 `MISS_MAX=5`(틀린그림 오답 터치·로직 틀린 칸)면 `failStage`. 그만두기·처음부터 다시는 건 하트를 잃음. 실수 수는 `S.miss`로 저장(이어하기 해도 유지). 운영진은 하트를 안 씀.
- 힌트 `HINT_MAX=5`(30분마다 1), 쿠키 하트 `CK_MAX=5`. 기존 보유가 5보다 많으면 `W()`·`C()`가 5로 맞춤. 실수 방패(`SHIELD_MAX=5`·`SHIELD_PRICE=200`, `P.shields`, 상점 본 게임·과자 둘 다): 실수가 `MISS_MAX`번째가 되면 `takeShield()`로 1개 쓰고 실수를 4로 되돌려 계속(`addMiss`·과자 판 `G.miss`), 안내 `shieldFx`.
- 클리어 코인 `STAR_COIN=[0,10,20,40]`(6.6~, 예전 25·50·100, 라운드 별점 기준). 라운드마다 코인 받은 별 수 `P.rounds[n].cs`를 두고 `STAR_COIN[새 별]-STAR_COIN[cs]`만 준다. `cs`가 없는 예전 기록은 `stars`만큼 받은 것으로 침. `CLEAR_COIN`(50)은 예전 소급 지급(`backpay`)에만 씀. 2.4 소급(`starBackpay`, 한 번만 `P.starpaid`): `cs` 없는 라운드마다 `STAR_COIN[stars]-plays×50`이 양수면 지급(빼지는 않음), 그 뒤 `cs=stars`.
- 업적 `ACH` (`LIST`: 진행·지역·별·칭호·끈기, 단계 `tiers`·보상 `rw`). 받은 단계는 `P.ach.got[id]`, 끈기 횟수 `P.ach.c.up/back`, 실패 표시 `P.ach.fail`. 지도 위쪽 메달 버튼(`#achBtn`, 받을 게 있으면 빨간 점). 칭호는 게임 종류별 별 3개 라운드 10·50·100·200 → 초보·중수·고수·달인(`P.title`, 업적 보상을 받아야 열림). 한 종류 라운드가 170개라 200(달인)은 `max`보다 커서 보이지만 비활성. 칭호는 `leaderboard.title`로 랭킹에 보냄(칸이 없으면 빼고 다시 보냄).
- 효과음 파일(5.5~): `sfx/<이름>.mp3` 40개(대표가 고른 결과 `sfx/picks.json`: 클로드·지팀장 시안). `SFX`가 첫 터치 때 AudioBuffer로 미리 받아 재생, 못 받으면 합성음(새 소리는 `ALT`로 비슷한 합성음). 소리 내용을 바꾸면 `SFX_V`를 올린다. `?sfx=off`면 합성음만(`?sfx=on` 되돌림). combo1~5=2~6연속, star1~3. 새 소리 연결: ready/go(`FX.ready`), zoom(🔍, 자동 tap 제외), xmark(로직 ×), piece(자리 바꿈)/fit(제자리), chal(도전 라운드 시작)/chalClear(첫 클리어), heaven(+도착 gallop, `playHeaven`), heart(하트·쿠키 구매), unlock(과자 구간 열림), candySit/candyX(과자), daily(오늘의 과자). 긴 소리(sail·heaven)는 건너뛰기·화면 숨김 때 멈춤, paint·xmark·candyX는 0.06초 간격.
- 효과음 `SFX`(Web Audio로 직접 합성, 소리 파일 없음): `SFX.play(이름)` — tap·pebble·hit·combo·miss·hint·paint·line·pick·piece·clear·star·fail·coin·buy·empty·sail·fly·open·badge. 사용자가 고른 시안(A 실로폰 기본, 조약돌·실수·힌트·날갯짓은 B 말랑 버블, 실패·코인·배 출발은 C 8비트). 버튼 소리는 document click 캡처로 자동(게임판·`data-sfx="none"` 제외). 켜기/끄기는 설정 `#stSfx`, localStorage `sekan-sfx`.
- 과자 나라 `CANDY` (Meowdoku 방식, 스타배틀 1개): 지도 오른쪽 가운데 `#candyGo` → 과자 마을 지도(`CANDY.showMap`, 300라운드 한 지역, 라운드당 82px, 발판 마카롱·젤리빈, 구간 장식 사탕 숲 1~100·쿠키 언덕 101~200·초콜릿 성 201~300). 왼쪽 가운데 '돌아가기', 오른쪽 가운데 '오늘의 과자'. 판 크기 6(1~20)·7(21~90)·8(91~140)·9(141~240)·10(241~300), 뒤로 갈수록 어려운 기법 필요(191~240·271~300은 구역 묶어 보기), 별 3개 시간 기준 칸 수×3+30초. 한 번 누르면 ×, 한 번 더 누르면 친구(틀리면 실수, 5번이면 실패), 친구가 앉으면 못 쓰는 칸에 점 표시, ×는 그어서 여러 칸. 쿠키 하트는 본 게임 하트와 따로(`P.candy.hearts`, 최대 10·10분마다 1·100코인). 오늘의 과자: 요일마다 크기(일10·월화7·수목8·금토9), 쿠키 안 씀, 처음 50코인·7일 연속 200·한 달 완성 500과 왕관 도장. 기록 `P.candy`(unlocked·rounds·daily·months), `mergeP`에서 합침. 랭킹 탭 '과자 나라'는 서버 함수가 없으면 '준비 중'. 본 게임과 연동: 구간 `PART`는 본 게임 `P.revealed`에 따라 열림(사탕 숲 처음부터·쿠키 언덕 푸른 바다·초콜릿 성 눈 덮인 산, `capTo`), 잠긴 구간 앞 안내판 `.cm-lock`, 본 게임에서 지역을 열 때 '과자 나라 ○○도 열렸어요!'. 업적 `ACH`에 '과자' 탭(candyClear·candyDaily)과 칭호 candyStar(과자 초보~달인), 과자 마을 지도에도 업적 버튼. 과자 나라 화면에서는 `CANDY.isOn()`이라 `showMenu`가 과자 마을을 그림(게임을 켜면 본 지도). **6.6: 600라운드**(`MAXC=600`): `PART`에 별사탕 하늘 301~450(11×11, 본 게임 별빛 하늘 z3)·구름 사탕섬 451~600(12×12, 하늘섬 z4) 추가, `TILES` 12개(11·12번째 `tileLemon`·`tileSoda`는 기존 그림 색만 바꾼 임시), 구간 장식 `DECO` 4·5번째는 기존 그림 섞음(임시), 업적 `candyClear` 단계 450·600 추가. 서버 `leaderboard_candy_check`는 SQL(2026-11-12)로 600·1800까지 넓힘(실행 전엔 `submit()`이 300·900 안으로 맞춰 보냄).
- 진행 기록 `P` (localStorage `sekan-progress`), 아이디 계정이면 Supabase `progress` 표와 동기화(`mergeP`). 기기 기록의 주인은 `sekan-owner`(아이디, 게스트는 ''): `afterLogin`은 게스트·같은 아이디 기록만 합치고, 다른 아이디 기록은 `sekan-stash:<아이디>`로 따로 두었다가 그 아이디로 다시 로그인할 때 합침. `doLogout`은 밀린 기록을 한 번 더 올리고(실패하면 stash) 기기 기록을 비움.
- 프로필 테두리 `FRAMES`(업적 `ACH.gotOf(id)` 단계로 열림, 운영진은 모두): `P.frame`·`P.frameAt`, 클래스 `fr fr-<id>`를 `.pf-av`·`.pf-big`에. 프로필 → 테두리 고르기(`openFrames`). 랭킹 서버에는 안 보냄.
- **프로필 카드·꾸미기(6.6)**: `openProfile()`은 시트가 아니라 전체 화면 `#pfScreen`(z24, 시트 z26 아래, 남의 카드 `.other`는 z28). 큰 캐릭터 카드 `stageHTML(av,sel,inner,cls)`(액자=`fr-<테두리>` 변수 `--fb/--fs`, 배경·받침·효과·동작·동행·대표 배지), 정보 칸 5개(순위·최고 라운드·별·총점·과자 나라; `RANK.me()`·`RANK.candyMe()`, 게스트·운영진은 안내 글), 카드 안 하단 업적(`ACH.open`)·꾸미기(`openDeco`) 버튼, ✕ 오른쪽 위. 꾸미기 모드 `openDeco`: 코인 탭 6(`COS.CAT` bg·base·tag·fx·move·comp, 종류마다 무료 1·200×3·500×4·1000×2, 동행 11마리 500, 눌러서 미리 보기→사기) + 업적 탭 3(테두리·칭호·대표 배지 3칸). 기록 `P.cos={own:['bg.candy',…],on:{bg,base,tag,fx,move,comp,g:['clear:3',…]},at}`(`COS.merge`가 `mergeP`에서 합침, 운영진은 모두 열림). 서버로는 `COS.pack()` 글자(`leaderboard.deco`)를 `submit()`이 보냄(칸이 없으면 빼고 다시 보냄). 남의 프로필: 랭킹 줄·지도 플레이어 목록·과자 랭킹 줄을 누르면 `openPlayerCard(row)`(읽기 전용, `COS.parse`가 정해진 목록 값만 받음, 아이디·코인은 안 보임). 동행 친구는 두 마리를 겹쳐 그림(`PAIRS_READY`에 '작은번호_큰번호'를 넣으면 `img/pair/pair<a>_<b>.webp` 그림을 씀), 대표 배지는 `BADGE_IMG`에 업적 id를 넣으면 `img/badge/badge_<id>.webp`, 없으면 메달 아이콘. 받침·배경·이름표·효과·동작은 모두 CSS(소품·받침·배경 그림은 지팀장 요청 뒤 교체). 서버 SQL은 `supabase/changes.sql` 2026-11-12(사용자가 실행).
- 지도 라운드 십이지는 60px(지금 라운드 70px), 지금 라운드 위에 내 프로필 핀 `mePin()`(`.me-pin`, 본 게임·과자 마을 지도 둘 다).
- 클리어 창 `#mRetry`(재도전, `retryRound`) → `startRound` (하트 1개 다시 걺).
- 프로필: 좌측 상단 `#profBtn`, 십이지 친구 얼굴 선택(`P.avatar`), 이름은 `ZODIAC.NAMES`(찍찍이·음메·어흥이·깡총이·미르·스르르·다그닥·몽실이·끼끼·꼬꼬·멍멍이·꿀꿀이).
- 지도 위 다른 플레이어(`OTHERS`): 서버 함수 `leaderboard_players`(랭킹에 기록이 있는 모든 사람, 게스트 포함·접속 여부 상관없음)로 받아 `best_round+1` 라운드 옆에 얼굴(최대 3개+N)과 닉네임, 누르면 그 라운드 목록. 1분 캐시, 함수가 없으면 아무것도 안 보임. 내 기록은 빼고 보임.
- 접속 신호: 세션이 이미 있는 사람만 45초마다 `presence` 표에 upsert(`RANK.beat`), 화면을 숨기거나 닫으면 online=false. 운영진 설정 → '접속 중인 사람'(`openOnline`)이 서버 함수 `presence_online()`(운영진 이메일만, 90초 안 신호)으로 10초마다 목록을 받음. 표·함수가 없으면 조용히 멈춤.
- 테스트 모드 `?qa=1`(ChatGPT 에이전트 QA용, `QA`): 운영진처럼 모든 라운드·선착장 열림·하트 안 씀, 랭킹·접속 신호 안 보냄, 기록은 localStorage `qa:` 칸에 따로(`store`의 `QK`). 탭 안에서 유지(sessionStorage), `?qa=0`으로 끔.
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
