# 작업 기록 — 틀린로직맞추기 (패치 6.6)

> 2026-11-12 기준. 이 저장소를 새 곳으로 옮겨도 이 파일과 `CLAUDE.md`·`docs/MEETING.md`만 읽으면 이어서 작업할 수 있게 정리했다.
> 게임 구조와 규칙은 `CLAUDE.md`, 회의 결정은 `docs/MEETING.md`, 이 파일은 **이번에 실제로 만든 것**의 기록이다.

## 한눈에
- 패치 6.5 → **6.6** (main 병합 34df3a8, 웹 배포 완료). 작업 브랜치 `patch-6.6`에서 만들고 한 번에 합침.
- 앱(APK/AAB)은 아직 안 만듦(서명 키 필요). `version.json`·`download/`는 그대로(6.5).
- 서버 SQL은 **사용자 실행 대기**: `supabase/changes.sql` 맨 아래 2026-11-12 구간, 실행 링크 `docs/SQL-6.6-링크.txt`.
- 새 그림은 지팀장(ChatGPT)에게 요청 중: `art-src/GPT-전달본.md`(장별 첨부 그림·요청문), `art-src/REQUEST-cosmetics.md`(계획).

## 6.6에서 한 일 (파일·함수 기준)
| # | 내용 | 주요 위치(`index.html`) |
|---|---|---|
| 1 | 하트·힌트·쿠키 하트 최대 5, 별 코인 10/20/40, 실수 방패(200코인, 실수 5번째를 1번 막음) | `HEART_MAX`·`HINT_MAX`·`CK_MAX`·`STAR_COIN`·`SHIELD_*`, `W()`·`C()`, `takeShield`·`shieldFx`, `addMiss`, 과자 판 `G.miss`, 상점 `openShop`·`CANDY.shop` |
| 2 | 301~330 로직 10×10 유지·dd 0.75/0.85, 로직 판 폭 최적화(단서 폭을 글자 수로 계산, 판을 화면 가장자리까지) | `ZONE_DIFF`, `renderLogic`, `.nono-wrap` |
| 3 | 퍼즐: 상한 7×7, 제자리 0개 섞기, 맞는 자리 고정, 회전 라운드(543부터 12라운드마다), 후반 비슷한 장면(361~ 50%·541~ 70%) | `ZONE_DIFF.jig`, `initJig`·`renderJig`·`jigClick`, `isRotate`·`isChal`·`jigBias`, `mixTheme(seed,bias)`·`PLAIN_BG` |
| 4 | 프로필 카드(큰 캐릭터·정보 칸 5·업적/꾸미기 버튼·✕ 오른쪽 위) + 꾸미기 모드 | `openProfile`·`openDeco`·`stageHTML`·`COS`, `#pfScreen`, `img/zbody/b0~11.webp` |
| 5 | 꾸미기 상품(배경·받침·이름표·효과·동작·동행 친구, 테두리·칭호·대표 배지) | `COS.CAT`, `P.cos`(`mergeP`에서 합침), `fxHTML`·`badgeHTML` |
| 6 | 남의 프로필 카드: 랭킹 줄·지도 목록·과자 랭킹 줄을 누르면 읽기 전용 | `bindCards`·`openPlayerCard`, `submit()`의 `deco`(+서버 칸 없을 때 대비) |
| 7 | 지역 이동 배 개선: 앞 파도 띠·위아래/기울기 분리·수면 링·꼬리 물결·물보라 | `playVoyage`, `.vy-heave`·`.vy-pitch`·`.vy-front`·`.vy-ring`·`.vy-wake` |
| 8 | 과자 나라 600라운드(301~450 11×11 별사탕 하늘, 451~600 12×12 구름 사탕섬) | `MAXC`·`PART`·`TILES`(12)·`decode`(36진수), 문제집 `tools/candy/gen_ext.py`, 업적 `candyClear` 450·600 |
| 9 | 누적 수정 #001~#005 | 4.4에서 이미 처리됨, #001은 재확인 |
| 10 | 패치 6.6 노트·번호·`sw.js` CACHE v96·CLAUDE.md 갱신 | `PATCH_NOTES`·`#introVer` |

## 새로 생긴 파일
- `tools/candy/gen_ext.py` — 과자 301~600 문제집 만들기(4코어 약 55분). `--apply`로 `index.html`에 붙임.
- `img/zbody/b0~11.webp` — 프로필 카드용 큰 몸 그림(460×600). `img/candy/tileLemon.webp`·`tileSoda.webp` — 11·12번째 과자 칸(임시, 기존 그림 색만 바꿈).
- `art-src/REQUEST-cosmetics.md`·`request-cosmetics.json`·`GPT-전달본.md`·`ref_candy_tiles.png` — 지팀장 그림 요청서(35번).
- `docs/SQL-6.6-링크.txt` — 서버 SQL을 SQL Editor에 채워 여는 링크. `docs/WORKLOG.md` — 이 파일.

## 임시로 둔 것 (지팀장 그림이 오면 교체)
- 동행 친구 쌍 그림 → 지금은 두 친구를 겹쳐 그림. 그림이 오면 `PAIRS_READY`에 '작은번호_큰번호' 추가(`img/pair/pair<a>_<b>.webp`).
- 대표 배지 → 메달 아이콘. 그림이 오면 `BADGE_IMG`에 업적 id 추가(`img/badge/badge_<id>.webp`).
- 과자 칸 11·12번째, 과자 나라 새 구간 장식(기존 그림 섞음), 받침·배경(CSS), 지역 이동 배(물결이 같이 그려진 그림 → 물결 없는 배 V1).

## 확인한 방법
- `python3 -m http.server 8765` + playwright로 390×844·360×640 캡처. 테스트 모드 `?qa=1`(기록은 `qa:` 칸).
- 로직 칸 크기(390폭): 7×7 51·8×8 43·10×10 33·12×12 29px. 더 키우려면 확대 미리보기(보류).
- 과자 11×11·12×12 판, 프로필·꾸미기(사기·미리 보기·동행·배지), 남의 카드(서버 응답을 흉내 낸 테스트), 방패 발동, 퍼즐 회전·고정, 쿠키 0 빈 판, 지역 이동 배를 실제 화면으로 확인.

## 남은 일
1. 서버 SQL 실행(사용자). 2. 지팀장 그림 35번 요청 → 오는 대로 누끼(`tools/matting/chroma.py`)·교체. 3. APK/AAB 빌드(서명 키 파일·비밀번호 필요). 4. 비공개 테스트 중 데이터를 보고 밸런스 재확인(서버 `best_round` 분포). 5. 광고는 프로모션 때. 6. 후보: 말풍선·배 스킨·칠한 칸 색·로직 확대 미리보기.

## 저장소를 새 GitHub 저장소로 옮길 때 바꿀 곳
- `index.html`의 `UPD`의 `BASE`(`https://yjeeeee0510-afk.github.io/teullin-logic/`), `README.md`의 플레이 주소, `privacy.html` 주소(Play Console에 적은 것), `version.json`·`download.html`의 다운로드 주소.
- GitHub Pages: 새 저장소 Settings → Pages → `main` 브랜치 루트.
- 서명 키(`teullinlogic-release.keystore`)와 `keystore.properties`는 저장소에 없으니 따로 옮길 것.

## 패치 6.7 (2026-11-14) — 지팀장 새 그림 교체
- 이동 장면: V1 배(물결 없음), V2C 물결 띠(거울로 이어 붙임)·뱃머리 물보라·물방울. 꼬리 물결은 끊겨 보여 뺌.
- 꾸미기: 받침 9종·배경 9장을 그림으로, 동행 쌍 66종 그림, 대표 배지 16종 그림. 소품(모자)은 캐릭터와 겹쳐 어색해서 없앰(원본 art-src/cos/C1·C2는 보관).
- 과자 칸 레몬·소다를 새 그림으로. 흰 바탕이라 바깥 윤곽만 따서 안쪽을 채움.
- 서버 SQL 변경 없음(꾸미기 글자에 소품 칸 안 씀).
- **6.7 Play 스토어 AAB 빌드 완료(2026-11-14)** → `dist/teullinlogic-play.aab`(19MB, versionCode 67, 커밋 안 함, Play Console에 업로드). 사이드로드 APK(`download/teullinlogic.apk`)·`version.json`·`download.html`도 6.7로 갱신.
  - 서명 키: 사용자 구글 드라이브 `앱서명키_보관용.zip`(키 파일+비밀번호 txt). 업로드 키 SHA-256 `ED:78:A7:35:4D:81:8B:F9:13:F0:BE:5E:A6:E4:8A:36:EB:1E:F7:58:9E:E1:43:2C:23:0E:35:35:9B:73:C7:AC`(Play Console 업로드 인증서와 일치 확인). Play 앱 서명 키(구글 보관)는 `4A:F2:C3:B5:…:00:0D`로 별개.
  - 새 세션에서 빌드하는 법: 환경 `teullin-logic`(dl.google.com·maven·gradle 주소 허용) → 드라이브에서 zip을 받아 키를 저장소 밖(`/root/keys`)에 두고 `app/android/keystore.properties`로 링크(.gitignore 제외) → Android SDK(cmdline-tools, `platforms;android-36`, `build-tools;36.0.0`)를 `ANDROID_HOME`에 설치 → `cd app && npm ci` → `python3 tools/app/release.py --play`(APK는 옵션 없이). Maven이 429(요청 과다)를 주면 40초쯤 쉬고 다시 실행하면 캐시로 이어진다.
- **서명 키 위치(2026-11-14 확인)**: 사용자 구글 드라이브 내 드라이브 최상위 `앱서명키_보관용.zip`(키 파일 `teullinlogic-release.keystore` + `서명키_비밀번호.txt`). 키 저장소·키 비밀번호는 같고 별칭 `teullinlogic`, keytool로 열림 확인. 새 세션은 Drive 커넥터로 내려받아(`download_file_content`가 파일로 저장) 새 빈 폴더에 풀고 `app/android/keystore.properties`(gitignore)를 만들어 쓰고, 끝나면 지운다. 비밀번호는 문서·커밋·대화에 쓰지 않는다.
- **인수인계(2026-11-14)**: 로컬(Cowork 등)에서 이어 작업할 수 있도록 `docs/HANDOFF-로컬작업.md`를 만듦. 결정·미확정·승인 원문은 `docs/DECISIONS.md`·`OPEN_ISSUES.md`·`APPROVAL_LOG.md`·`CHANGELOG.md`.
- **운영진 닉네임 수정(2026-11-14, A-006)**: 운영진은 랭킹 기록이 없어 닉네임이 서버에 안 남던 문제를 고침. 로그인 때 접속 상태 표(presence)에서 닉네임을 복원하고, 접속 신호가 닉네임을 빈 값으로 덮어쓰지 않게 함. 가짜 서버 검사로 복원·랭킹 미전송·주소 토큰 정리 확인. 실서버·실기기는 미검증. sw.js CACHE v99.
- **패치 6.9(2026-11-14, A-007)**: 운영진 모드 스위치(isStaff/isAdmin 분리), 우편함(받기·모두 받기·삭제·만료·새 우편 알림), 운영진 우편 보내기·보낸 기록, 하트·쿠키 하트 5개 초과 보관(보정 제거), 설정창 구글 문구 정리. 서버: supabase/patch-6.9-mailbox.sql(PGlite로 로컬 시험 통과, 실서버 미실행). 가짜 서버 브라우저 시험: 수령·중복·재로드 보관·운영진 모드·발송 확인·게스트/일반 계정 권한 통과. sw.js CACHE v100.
- **패치 7.0(2026-11-14, A-008)**: 결제 뼈대를 스위치 꺼짐 상태로 배포. 서버 supabase/patch-7.0-payments.sql(app_flags·products·purchases·함수, PGlite 시험 통과)·functions/verify-purchase(초안·미배포·미검증). 클라이언트 특별 상점 '준비 중', 서버 기록 구매 받기(PAY.sync). 가짜 서버 시험: 스위치 켜져도 웹은 잠김, 구매분 1회 지급. 실제 Play 결제·검증 서버는 미검증. sw.js CACHE v101.
- **패치 7.1(2026-11-14, A-009)**: 보상형 광고 뼈대를 스위치 꺼짐으로 배포. 광고 모듈(ADS: 종류별 하루 한도, P.ads 저장·합치기, 공급자 계약 RewardedAds), 하트·쿠키 하트·힌트·이어하기(본 게임·과자 나라)·코인 2배 버튼(광고 켜졌을 때만 보임). 서버 SQL 없음(7.0의 app_flags 사용). 가짜 공급자 시험 통과: 스위치 꺼짐/웹/운영진은 버튼 없음, 끝까지 못 보면 보상 없음, 한도 초과 시 숨김, 이어하기 1회·시간 이어감. 코인 2배(본 게임·과자 나라)와 과자 나라 이어하기는 코드 검토만(실행 미검증). 실제 AdMob은 미검증. sw.js CACHE v102.
- **패치 7.2(2026-11-14)**: Play 광고 ID 선언 문제(Play Console '광고 ID 선언이 불완전') 대응. 구글 로그인 플러그인이 끌고 온 AD_ID·ACCESS_ADSERVICES_* 권한 4개를 AndroidManifest에서 제거(광고 미사용). Play 앱 콘텐츠 > 광고 ID는 '사용 안 함'으로 선언. 광고를 켜는 패치(O-014)에서 AD_ID 권한을 다시 넣고 '사용함'으로 바꿀 것. versionCode 71은 Play에 이미 등록되어 72로 올림. sw.js CACHE v103.
