# 앱 이미지 요청문 (ChatGPT, 한 장씩)

첨부: 게임 지도 화면 캡처 1장 + 십이지 친구 얼굴 그림 1~2장 + 물건 그림 1장(그림체 맞추기용).
받은 그림은 `art-src/app/`에 아래 파일 이름으로 저장 → Claude가 `python3 tools/app/make_res.py`로 앱에 넣음.

공통 그림체 (모든 요청 끝에 붙이기):
Cute soft 3D clay toy style, rounded chunky shapes, gentle gloss, bright pastel colors, light from the top-left, same art style as the attached reference images. No text, no letters, no numbers, no logos, no watermark.

---

## 1. icon.png — 앱 아이콘 (1024×1024)
A square mobile game app icon, 1024x1024, full-bleed artwork that fills the whole square (no rounded corners, no border, no transparent edges; the phone will round the corners itself). Center: a cute chubby green baby turtle character (the game's mascot friend from the attached reference) peeking out happily, holding a big golden magnifying glass. Behind it, slightly overlapping: a small 3x3 nonogram grid tile with a few filled pastel cells and one colorful jigsaw puzzle piece. Background: soft sky-blue to mint gradient with a few tiny sparkles. Big, simple, readable shapes that still read clearly at 48x48 pixels; the character and magnifying glass take up about 70% of the icon. + 공통 그림체

## 2. icon_fg.png — 적응형 아이콘 앞 그림 (1024×1024, 투명 바탕)
The same mascot artwork as icon.png (turtle with magnifying glass, small nonogram tile and puzzle piece), but ONLY the characters and objects on a fully transparent background (PNG with alpha), no background color. Keep every important part inside the central 66% circle (about 680x680 in the middle); the outer area must be empty because phones crop it into circles, squircles or rounded squares. Same position and size feel as the full icon. + 공통 그림체

## 3. icon_bg.png — 적응형 아이콘 뒤 그림 (1024×1024)
Only the background of the app icon: the soft sky-blue to mint gradient with a few tiny sparkles and a faint soft cloud at the bottom, filling the whole 1024x1024 square, no characters, no objects. + 공통 그림체

## 4. splash.png — 앱 시작 화면 (1080×1920 세로)
A vertical 1080x1920 mobile game splash screen background: a dreamy pastel world map seen from above, a small flower island at the bottom, a sea in the middle with a tiny orange sailboat, a snowy island, a starry purple island and a floating sky island toward the top, all small and soft. Leave a calm empty area in the center (about 600x600) where the app logo will be placed, keep the busiest details near the top and bottom edges. + 공통 그림체

## 5. feature.png — 플레이스토어 대표 그림 (1024×500, 나중에 스토어 출시용)
A wide 1024x500 promotional banner for a cute puzzle game: on the left the green turtle mascot with a golden magnifying glass, in the middle three floating cards showing a spot-the-difference picture, a nonogram grid and a jigsaw puzzle, on the right a small candy house and a winged golden ship flying to a floating sky island. Soft pastel sky background. Leave the top-left third fairly simple for a title that will be added later. + 공통 그림체

---

### 확인할 점 (받은 뒤 Claude가 검사)
- icon.png를 48×48로 줄여도 거북이와 돋보기가 알아보이는지
- icon_fg.png의 중요한 부분이 가운데 66% 원 안에 있는지, 바탕이 진짜 투명한지
- 글자·숫자·로고가 들어가지 않았는지
