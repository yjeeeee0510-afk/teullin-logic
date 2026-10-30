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

아직 없는 원본: 꽃 언덕(flower)·푸른 바다(sea·sea2)·눈 덮인 산(snow)·별빛 하늘(night) 물건 모음, 하늘섬 구름(sky/clouds.png, 초록 바탕),
지역 이동 섬 4개(islFlower·islNight·islSea·islSnow)와 배(vyBoat*), 꽃 언덕~별빛 하늘 배경·지도 그림.
