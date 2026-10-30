# 전체 그림 다시 만들기 — 장 계획 (2026-10-30, 6개 이하 버전)

ChatGPT에 물건 모음 32장 + 배경 24장을 요청. 영어 요청문 전체는 `art-src/request.json`.
받은 그림은 `art-src/new/<장 이름>.png`(예: F1.png, BG03.png)로 저장하고, 아래 칸 순서(1줄 왼→오른, 3칸씩)대로 누끼를 딴다. wingShip 은 vyWingShip 을 복사.

| 장 | 바탕 | 칸 순서 |
|---|---|---|
| F1 | 파랑 #0047FF | windmill cottageRed blossomPink blossomWhite blossomYellow treeRound |
| F2 | 파랑 #0047FF | flowersPink flowersYellow flowersWhite tulipRed tulipYellow tulipPurple |
| F3 | 파랑 #0047FF | mushroomRed fenceWhite beehive hayBale butterfly sun |
| F4 | 초록 #00B140 | cottageBlue cottagePurple kite puffA puffB puffC |
| S1 | 초록 #00B140 | lighthouse umbrellaRed umbrellaBlue umbrellaYellow sandcastle gull |
| S2 | 초록 #00B140 | shellPink shellWhite starfishOrange starfishPink crab swimRing |
| S3 | 마젠타 #FF00FF | beachHutBlue beachHutPink beachHutMint bucketBlue bucketGreen flowersBlue |
| S4 | 파랑 #0047FF | palmA palmB sled skiSign featherGold owlPost |
| S5 | 마젠타 #FF00FF | boatOrange boatBlue boatPurple dock buoy fish |
| S6 | 마젠타 #FF00FF | rockBig rockMid rockSmall vyBoatOrange vyBoatBlue vyBoatPurple |
| W1 | 파랑 #0047FF | cabinRed cabinBrown cabinGreen pineSnowA pineSnowB snowBush |
| W2 | 파랑 #0047FF | snowmanRed snowmanBlue snowmanGreen snowballs skyTree bushNight |
| W3 | 초록 #00B140 | igloo pineSnowC penguin iceBlue icePurple moonFull |
| N1 | 초록 #00B140 | castleLilac castleBlue castlePink observatory treeNightPurple cloudNight |
| N2 | 초록 #00B140 | glowMushBlue glowMushPink gemPurple gemBlue gemPink starBig |
| N3 | 초록 #00B140 | lanternOrange lanternPink moonCrescent starWish planetRing featherPurple |
| N4 | 마젠타 #FF00FF | lampYellow lampBlue treeNightTeal glowMushGreen planetSmall rainbowBridge |
| K1 | 초록 #00B140 | balloonRed balloonBlue kiteYellow pinwheelPink pinwheelBlue airship |
| K2 | 파랑 #0047FF | skyHouse bellTower weatherVane birdHouse kiteGreen wingMail |
| K3 | 초록 #00B140 | skyWhale starJar vyShip vyWing vyWingShip |
| K4 | 초록 #00B140 | skyCloudA skyCloudB skyCloudC skyCloudD skyCloudE skyCloudF |
| K5 | 초록 #00B140 | pebCloudA pebCloudB pebCloudC pebCloudD cookieFull cookieEmpty |
| I1 | 마젠타 #FF00FF | islFlower islSea islSnow |
| I2 | 마젠타 #FF00FF | islNight islSky |
| C1 | 파랑 #0047FF | cdLollyTree cdGummyBears cdCandyFlower cdJellyMush cdCottonBush cdCandyCane |
| C2 | 파랑 #0047FF | cdCookieHouse cdCupcake cdCake cdDonut cdCream cdMacaronTower |
| C3 | 파랑 #0047FF | cdChocoCastle cdChocoFountain cdChocoBridge cdTruffle cdChocoTree cdClockTower |
| C4 | 파랑 #0047FF | stampCookie stampMacaron stampDonut stampCandy stampJelly stampCrown |
| C5 | 파랑 #0047FF | padMacPink padMacMint padMacYellow padJelly padBeanGreen padBeanPurple |
| C6 | 파랑 #0047FF | padMallow padCookie tileMatcha tileMint btnCandyHouse btnCookieBoat |
| C7 | 초록 #00B140 | tileStrawberry tileChoco tileButter tileBlueberry tileGrape tileOrange |
| C8 | 초록 #00B140 | tileWafer tileCherry btnCandyShop |
| U1 | 파랑 #0047FF | icoHeart icoCoin icoHint icoStar icoLock icoMedal |
| U2 | 마젠타 #FF00FF | icoTrophy icoGear icoCart icoSpot icoLogic icoPuzzle |
| U3 | 초록 #00B140 | icoMenu icoStarEmpty icoHeartEmpty |

화면 아이콘(U1~U3)은 index.html 의 ICON·TYPE_ICON·TROPHY·GEAR·LOCK·STAR 와 메뉴 버튼 SVG를 대체한다(64px WebP).

| 배경 | 파일 | 용도 |
|---|---|---|
| BG01 | scene_flowerhill | 꽃 언덕 틀린그림 배경 |
| BG02 | gamebg_flowerhill | 꽃 언덕 인게임 배경 |
| BG03 | mapfloor_flowerhill | 꽃 언덕 지도 바닥 |
| BG04 | shore_flowerhill | 꽃 언덕 지도 끝 바닷가 |
| BG05 | scene_beach | 푸른 바다 틀린그림 배경 |
| BG06 | gamebg_sea | 푸른 바다 인게임 배경 |
| BG07 | mapfloor_sea | 푸른 바다 지도 바닥 |
| BG08 | shore_sea | 푸른 바다 지도 끝 바닷가 |
| BG09 | scene_snow | 눈 덮인 산 틀린그림 배경 |
| BG10 | gamebg_snow | 눈 덮인 산 인게임 배경 |
| BG11 | mapfloor_snow | 눈 덮인 산 지도 바닥 |
| BG12 | shore_snow | 눈 덮인 산 지도 끝 바닷가 |
| BG13 | scene_night | 별빛 하늘 틀린그림 배경 |
| BG14 | gamebg_night | 별빛 하늘 인게임 배경 |
| BG15 | mapfloor_night | 별빛 하늘 지도 바닥 |
| BG16 | shore_night | 별빛 하늘 지도 끝 바닷가 |
| BG17 | scene_sky | 하늘섬 틀린그림 배경 |
| BG18 | gamebg_sky | 하늘섬 인게임 배경 |
| BG19 | mapfloor_sky | 하늘섬 지도 바닥 |
| BG20 | shore_sky | 하늘섬 지도 끝 바닷가 |
| BG21 | voyage_sea | 기타 지역 이동 바다 |
| BG22 | candy_bg | 기타 과자 나라 게임 배경 |
| BG23 | candy_floor | 기타 과자 나라 지도 바닥 |
| BG24 | candy_gate | 기타 과자 나라 마을 입구 |
