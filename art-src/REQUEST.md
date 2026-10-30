# 전체 그림 다시 만들기 — 장(sheet) 계획 (2026-10-30)

ChatGPT에 물건 모음 16장 + 배경 24장을 요청. 각 장은 3줄×4칸(읽는 순서: 위 줄부터, 왼→오른).
바탕: B = 파랑 #0047FF, G = 초록 #00B140, M = 마젠타 #FF00FF (물건 가장자리 색과 겹치지 않게 장마다 고름).
받은 그림은 art-src/new/<장 이름>.png 로 저장하고, 이 순서대로 누끼를 딴다. wingShip 은 vyWingShip 을 복사.

| 장 | 바탕 | 물건 (읽는 순서) |
|---|---|---|
| B1 | 파랑 | windmill cottageRed blossomPink blossomWhite blossomYellow treeRound beehive hayBale |
| B2 | 파랑 | flowersPink flowersYellow flowersWhite tulipRed tulipYellow tulipPurple mushroomRed fenceWhite butterfly puffA puffB puffC |
| B3 | 파랑 | palmA palmB cabinRed cabinBrown cabinGreen pineSnowA pineSnowB snowmanRed snowmanBlue snowmanGreen snowBush snowballs |
| B4 | 파랑 | skyHouse bellTower weatherVane birdHouse skyTree kiteGreen owlPost bushNight sled skiSign featherGold sun |
| B5 | 파랑 | cdLollyTree cdGummyBears cdCandyFlower cdJellyMush cdCottonBush cdCandyCane cdCookieHouse cdCupcake cdCake cdDonut cdCream cdMacaronTower |
| B6 | 파랑 | cdChocoCastle cdChocoFountain cdChocoBridge cdTruffle cdChocoTree cdClockTower stampCookie stampMacaron stampDonut stampCandy stampJelly stampCrown |
| B7 | 파랑 | padMacPink padMacMint padMacYellow padJelly padBeanGreen padBeanPurple padMallow padCookie tileMatcha tileMint btnCandyHouse btnCookieBoat |
| G1 | 초록 | cottageBlue cottagePurple kite lighthouse umbrellaRed umbrellaBlue umbrellaYellow sandcastle shellPink shellWhite starfishOrange starfishPink |
| G2 | 초록 | crab swimRing gull igloo pineSnowC penguin iceBlue icePurple moonFull moonCrescent starBig starWish |
| G3 | 초록 | castleLilac castleBlue castlePink observatory treeNightPurple glowMushBlue glowMushPink gemPurple gemBlue gemPink lanternOrange lanternPink |
| G4 | 초록 | balloonRed balloonBlue kiteYellow pinwheelPink pinwheelBlue airship wingMail skyWhale featherPurple starJar planetRing cloudNight |
| G5 | 초록 | skyCloudA skyCloudB skyCloudC skyCloudD skyCloudE skyCloudF pebCloudA pebCloudB pebCloudC pebCloudD vyShip vyWing |
| G6 | 초록 | tileStrawberry tileChoco tileButter tileBlueberry tileGrape tileOrange tileWafer tileCherry cookieFull cookieEmpty btnCandyShop vyWingShip |
| M1 | 마젠타 | beachHutBlue beachHutPink beachHutMint bucketBlue bucketGreen flowersBlue planetSmall lampYellow lampBlue treeNightTeal glowMushGreen rainbowBridge |
| M2 | 마젠타 | boatOrange boatBlue boatPurple dock rockBig rockMid rockSmall buoy fish vyBoatOrange vyBoatBlue vyBoatPurple |
| M3 | 마젠타 | islFlower islSea islSnow islNight islSky (위 3개, 아래 2개) |

배경 24장(지역 5 × 4종 + 바다 1 + 과자 나라 3): 지역마다 scene(틀린그림 배경, 가로 1536×1024) · gamebg(인게임 배경, 세로 1024×1536) ·
mapfloor(지도 바닥, 세로 1024×1536, 위아래 이어짐) · shore(지도 끝 바닷가, 가로 1536×1024), voyage sea(옆에서 본 바다, 가로),
candy bg(세로)·floor(세로, 위아래 이어짐)·gate(가로).
