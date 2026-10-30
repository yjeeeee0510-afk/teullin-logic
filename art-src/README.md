# 게임 그림 원본 (사용자가 ChatGPT로 만든 그림)

누끼·크기 조정은 항상 이 폴더의 원본에서 다시 한다. 게임에 들어가는 결과물은 `img/` 아래.
파일 이름은 누끼 도구(`tools/matting/*.py`)가 찾는 이름에 맞춘다.

| 폴더 | 원본 | 바탕 | 나오는 게임 그림 | 도구 |
|---|---|---|---|---|
| candy | candy.png | 파랑 | cdLollyTree·cdGummyBears·cdCandyFlower·cdJellyMush·cdCottonBush·cdCandyCane | matting/candy.py |
| candy | cake.png | 파랑 | cdCookieHouse·cdCupcake·cdCake·cdDonut·cdCream·cdMacaronTower | matting/candy.py |
| candy | choco.png | 파랑 | cdChocoCastle·cdChocoFountain·cdChocoBridge·cdTruffle·cdChocoTree·cdClockTower | matting/candy.py |
| candy | stamps.png | 파랑 | stampCookie·stampMacaron·stampDonut·stampCandy·stampJelly·stampCrown | matting/candy.py |
| candy | pads.png | 파랑 | padMacPink·padMacMint·padMacYellow·padJelly·padBeanGreen·padBeanPurple·padMallow·padCookie | matting/candy.py |
| candy | heart.png | 파랑 | cookieFull·cookieEmpty | matting/candy.py |
| candy | buttons.png | 파랑 | btnCandyHouse·btnCookieBoat·btnCandyShop | matting/candy.py |
| candy | tiles.png | 흰색 | tileStrawberry·tileChoco·tileButter·tileMint·tileBlueberry·tileGrape·tileOrange·tileMatcha·tileWafer·tileCherry | matting/candy.py |
| candy | floor.png / gate.png / bg.png | – | candyFloor.jpg / candyGate.jpg / candyBg.jpg | matting/candy.py |
| candy | sweets_extra.png | 빛 번진 바탕 | (아직 안 씀: 과자 15개) | – |
| sky | items.png | 흰색 | balloonRed·balloonBlue·kiteYellow·kiteGreen·pinwheelPink·pinwheelBlue·skyHouse·bellTower·weatherVane·birdHouse·airship·wingMail·rainbowBridge·skyTree·skyWhale·featherGold·featherPurple·starJar | matting/sky.py |
| sky | isl.png | 흰색 | islSky | matting/sky.py |
| sky | ship.png | 투명 | vyShip·vyWing·vyWingShip | matting/sky.py |
| sky | scene.png | – | img/scenes/skyisland.jpg (틀린그림·퍼즐 배경) | – |
| sky | game_bg.png | – | img/bg/zone4-sky.jpg (인게임 배경) | – |
| sky | map_floor.png / map_shore.png | – | img/map/zone4.jpg / shore4.jpg (지도 바닥·바닷가) | – |
| misc | mixed.png | 흰색 | 섞인 모음: 하늘섬·날개 배·꽃 언덕 섬·성·집·열기구·비행선·오두막·통나무집·꽃나무·게·나비·보석·깃털·빛나는 버섯 | – |

| sky | clouds.png | 초록 | skyCloudA~F(구름 6)·pebCloudA~D(구름 발판 4) | matting/sky.py |
| flower | flower.png | 흰색 | windmill·cottageRed/Blue/Purple·blossomPink/White/Yellow·treeRound·flowersPink/Yellow/Blue/White·tulipRed/Yellow/Purple·mushroomRed·fenceWhite·beehive·hayBale·butterfly·kite | matting/matte3.py |
| flower | scene.png | – | img/scenes/flowerhill.jpg (틀린그림·퍼즐 배경) | – |
| flower | map_floor.png / map_shore.png | – | img/map/zone0.jpg / shore0.jpg | – |
| sea | sea.png | 흰색 | lighthouse·beachHutBlue/Pink/Mint·palmA/B·umbrellaRed/Blue/Yellow·sandcastle·shellPink/White·starfishOrange/Pink·crab·bucketBlue/Green·swimRing·gull (게임에 쓰는 버전) | matting/matte3.py |
| sea | sea_v1.png | 흰색 | 같은 물건의 다른 시안(오두막에 튜브) — 안 씀 | – |
| sea | sea2.png | 흰색 | boatOrange/Blue/Purple(위에서 본 배)·dock·rockBig/Mid/Small·buoy·fish | matting/matte3.py |
| sea | scene.png | – | img/scenes/beach.jpg | – |
| sea | map_floor.png / map_shore.png | – | img/map/zone1.jpg / shore1.jpg | – |
| snow | scene.png | – | img/scenes/snowmount.jpg | – |
| snow | map_floor.png / map_shore.png | – | img/map/zone2.jpg / shore2.jpg | – |
| night | map_floor.png / map_shore.png | – | img/map/zone3.jpg / shore3.jpg | – |
| voyage | isl4.png | 흰색 | islFlower·islSea·islSnow·islNight (지역 이동 섬) | – |
| voyage | boats.png | 투명 | vyBoatOrange·vyBoatBlue·vyBoatPurple | – |
| voyage | sea.png | – | img/voyage/sea.jpg (옆에서 본 바다) | – |

| snow | snow.png | 흰색 | cabinRed/Brown/Green·igloo·pineSnowA/B/C·snowmanRed/Blue/Green·penguin·sled·snowBush(큰 것)·작은 눈 덤불·iceBlue·icePurple·snowballs·skiSign | matting/matte3.py |
| night | night.png | 흰색 | castleLilac(성)·observatory·lampYellow·lampBlue·treeNightPurple·treeNightTeal·glowMushBlue/Pink/Green·gemPurple/Blue/Pink·lanternOrange/Pink·bushNight·owlPost | matting/matte3.py |
| night | scene.png | – | img/scenes/nightsky.jpg (지금 쓰는 것과 가장 비슷) | – |
| night | scene_a.png / scene_c.png | – | 별빛 하늘 배경 다른 시안 (반딧불·구름 없음) — 안 씀 | – |
| misc | skyitems.png | 흰색 | puffA/B/C·sun·moonFull·moonCrescent·starBig·starWish·planetRing·planetSmall·cloudNight (하늘 장식) | matting/matte3.py |
| zodiac | face01~12_*.png | 투명 | 십이지 친구 얼굴(프로필·지도) — index.html ZIMG | – |
| zodiac | faces.png / bodies.png | – | 십이지 얼굴·몸 모음 (원본 확인용) | – |

남은 원본: 지역별 인게임 배경(img/bg/zone0~3 — 하늘섬 것은 sky/game_bg.png).
