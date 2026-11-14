# 인수인계: 클라우드 세션 → 로컬(Cowork 등) 작업 (2026-11-14)

새 세션은 **이 파일 → `CLAUDE.md` → `docs/DECISIONS.md` → `docs/OPEN_ISSUES.md`** 순서로 읽고 시작한다.
(대표 운영 지침은 계정 설정에 있으므로 어느 환경에서나 적용된다: 대표 승인 기반·증분 기록·개발 전 변경 계획 보고.)

## 1. 지금 상태 (2026-11-14)
- 웹(GitHub Pages)·앱 **패치 6.7** 반영 완료. Play 스토어용 AAB(versionCode 67)와 사이드로드 APK 빌드·서명 확인 완료. AAB는 대표가 Play Console 비공개 테스트에 올리는 중.
- 이 클라우드 세션의 작업 브랜치: `claude/magical-mayer-ozvkfj` (docs 기록 포함). `main`에는 6.7 APK·`version.json`까지만 병합됨(PR #1). **새 docs 기록(승인 로그·결정·변경 이력·이 파일)은 브랜치에만 있다** → 로컬에서는 이 브랜치를 받거나, 대표 승인 후 `main`에 병합한다.
- 코드는 6.7 그대로. **구현 착수 전**이며 아래 승인된 기획만 기록됨.

## 2. 확정된 기획 (자세한 건 `docs/DECISIONS.md`, 원문은 `docs/APPROVAL_LOG.md`)
| ID | 요약 |
|---|---|
| D-001 | 보상형 광고 B안(하트·힌트·이어하기·코인 2배), 프로모션 때 켬 |
| D-002 | 결제 B안(코인 묶음·꾸미기 패키지·스타터 팩), Play판 한정, 서버 영수증 검증 |
| D-003 | 로그인을 **구글 전용**으로 교체 |
| D-004 | 운영진 = `yjeeeee0510@gmail.com` 한 개 |
| D-005 | 순서: 구글 로그인 → 우편함·운영진 발송·운영진 모드 → 결제 → 광고 |
| D-006 | 운영진 모드 A: 보기용 스위치(진행 기록 불변) |
| D-007 | 우편함 B안(운영진·시스템 우편, 받기·모두 받기·만료) |
| D-008 | 운영진 발송 B안(개별·전체·조건 대상, 발송 기록) |
| D-009 | 우편 수령분은 최대 5를 넘어도 보관 |

## 3. 다음 작업 (대표 승인 필요)
1. **패치 6.8 구글 로그인** — 변경 계획은 대화에서 보고함(수정 대상: `index.html`의 `RANK` 로그인 호출·`afterLogin`·`doLogout`·`ADMIN_IDS`, `app/` 구글 로그인 플러그인, `privacy.html`, 서버 SQL). **개발 착수 승인은 아직 받지 않음.**
2. 패치 6.9 우편함·운영진 발송·운영진 모드.
3. 결제 → 광고.

### 미확정 (대표 결정 필요, `docs/OPEN_ISSUES.md`)
- O-001 기존 아이디 사용자 기록 이전(추천: 첫 실행 '기존 계정 연결' 안내 + 아이디 로그인 후 구글 연결, 서버 함수로 두 계정 확인)
- O-002 게스트 유지 여부(추천: 유지, 우편함·랭킹은 구글 로그인만)
- O-008 전체 발송 범위(추천: 보관 기간 안 신규 가입자도 받음)
- O-004 대표가 할 설정: Google Cloud OAuth 클라이언트(웹·안드로이드, 업로드 키 SHA-256 `ED:78:A7:35:…`와 Play 앱 서명 키 `4A:F2:C3:B5:…`의 SHA-1 등록), Supabase Authentication → Providers → Google. **클라이언트 시크릿은 대화·저장소에 쓰지 않는다.**

## 4. 로컬에서 시작하기
```bash
git clone -b claude/magical-mayer-ozvkfj https://github.com/yjeeeee0510-afk/teullin-logic.git
cd teullin-logic
python3 -m http.server 8765   # http://localhost:8765/?qa=1 로 확인(테스트 모드)
```
- 게임 확인에는 Node·Python3만 있으면 된다. 앱 빌드까지 하려면 Java 21, Android SDK(`platforms;android-36`, `build-tools;36.0.0`), `cd app && npm ci`.
- 클라우드 세션 전용 사항이므로 로컬에서는 무시: npm 프록시 옵션, `/root/keys`, Maven 429 재시도.
- 앱 빌드 순서: `python3 tools/app/release.py --play`(AAB, `dist/`, 커밋 안 함) / `python3 tools/app/release.py`(사이드로드 APK, 커밋).

## 5. 비밀·키 (저장소에 절대 넣지 않는다)
- 서명 키: 대표 구글 드라이브 `틀린로직맞추기` 상위 `앱서명키_보관용.zip`(키 파일 + 비밀번호 txt). 로컬 빌드 시 저장소 밖에 풀고 `app/android/keystore.properties`(.gitignore됨)를 만든다. 끝나면 임시 사본을 지운다. 비밀번호는 문서·커밋·대화에 쓰지 않는다.
- Supabase: `rank-config.js`에는 공개(publishable) 키만. secret/service_role 키 금지.
- 운영 DB 변경(SQL)은 대표가 SQL Editor에서 직접 실행. SQL을 만들면 채워진 링크를 열어 준다(`CLAUDE.md` 참고).

## 6. 작업 규칙 요약
- 승인 없이 코드·기능·수치를 바꾸지 않는다. 승인 → 원문(`APPROVAL_LOG`) → 결정(`DECISIONS`) → 충돌 확인 → 저장 검증 → 보고.
- 플레이어에게 보이는 변경은 패치 번호 +0.1, `PATCH_NOTES`·`#introVer`·`sw.js` CACHE 갱신(`CLAUDE.md` 참고).
- 실행하지 않은 테스트는 '미검증'으로 보고한다.
- 로컬에서는 `main` 직접 푸시 가능 여부를 환경 설정에 따라 확인하고, 클라우드 세션은 지정 브랜치에만 푸시했다.

## 7. 새 세션 첫 메시지 예시
> docs/HANDOFF-로컬작업.md를 읽고 DECISIONS·OPEN_ISSUES 기준으로 이어서 진행해 줘. 패치 6.8 구글 로그인 변경 계획부터 다시 보고해 줘.
