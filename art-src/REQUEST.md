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

## 천국 (6지역, 511~720라운드) — 2026-11-04 추가

받은 그림은 `art-src/heaven/<장 이름>.png`(H1.png, BG25.png …)로 저장. 영어 요청문은 `art-src/request.json`.

| 장 | 바탕 | 칸 순서 |
|---|---|---|
| H1 | #00B140 | heavenGate chapelGold chapelBlue chapelPink lightTreeGold lightTreeWhite |
| H2 | #0047FF | harpGold harpSilver fountainLight chimeGold chimeSilver cloudBench |
| H3 | #FF00FF | lilyWhite lilyGold lilyPink featherWhite featherBlue candleLight |
| H4 | #00B140 | doveWhite haloGold haloPink sunHeaven lanternHeaven stairCloud |
| H5 | #00B140 | pebHeavenA pebHeavenB pebHeavenC pebHeavenD goldCloudA goldCloudB |
| I3 | #FF00FF | islHeaven heavenDock |

| 배경 | 파일 | 용도 |
|---|---|---|
| BG25 | scene_heaven | 천국 틀린그림 배경 |
| BG26 | gamebg_heaven | 천국 인게임 배경 |
| BG27 | mapfloor_heaven | 천국 지도 바닥 |
| BG28 | shore_heaven | 천국 지도 끝 |
| H6 | #00B140 | pegBody pegWing carriage pegCarriage flyCloudA flyCloudB |
| BG29 | voyage_heaven | 하늘섬→천국 천마 이동 하늘(좌우 이음) |

## 선착장 (지역별) — 2026-11-04
받은 그림은 `art-src/dock/D1.png`~`D6.png`. 칸 순서: 왼쪽·가운데·오른쪽. 배는 `B1.png`(1줄 boatOrange boatBlue boatPurple, 2줄 wingShip pegCarriageTop) — 이동 장면 배와 같은 모양.

| 장 | 바탕 | 칸 순서 |
|---|---|---|
| D1 | #FF00FF | dockFlower decoFlowerA decoFlowerB |
| D2 | #FF00FF | dockSea decoSeaA decoSeaB |
| D3 | #0047FF | dockSnow decoSnowA decoSnowB |
| D4 | #00B140 | dockNight decoNightA decoNightB |
| D5 | #FF00FF | dockSky decoSkyA decoSkyB |
| D6 | #00B140 | dockHeaven decoHeavenA decoHeavenB |

## 십이지 리뉴얼 (2026-11-05)

같은 ChatGPT 대화에서 Z1→Z4 순서로, 뒤 장엔 앞 결과를 붙여 얼굴·몸을 맞춘다. 받은 그림은 `art-src/new/Z1.png`~`Z4.png`.
얼굴 `zFace0~11` → `ZIMG.face`, 몸 `zBody0~11` → `ZIMG.body` (순서는 `ZODIAC.NAMES`).

| 장 | 바탕 | 칸 순서 |
|---|---|---|
| Z1 | 파랑 #0047FF | 얼굴: 찍찍이 음메 어흥이 깡총이 미르 스르르 |
| Z2 | 초록 #00B140 | 얼굴: 다그닥 몽실이 끼끼 꼬꼬 멍멍이 꿀꿀이 |
| Z3 | 파랑 #0047FF | 몸: 찍찍이 음메 어흥이 깡총이 미르 스르르 |
| Z4 | 초록 #00B140 | 몸: 다그닥 몽실이 끼끼 꼬꼬 멍멍이 꿀꿀이 |
