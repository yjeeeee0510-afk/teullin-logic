// 틀린로직맞추기 지역 그림 (직접 그린 SVG). 평면 스타일, 왼쪽 밝고 오른쪽 어두운 면으로 입체감.
const S = {}; // sprites: name -> {w,h,svg}
const B = {}; // backgrounds 800x600
const sp = (name, w, h, body) => { S[name] = { w, h, svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">${body}</svg>` }; };
const bg = (name, body) => { B[name] = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">${body}</svg>`; };
const lg = (id, a, b, x2 = 0, y2 = 1) => `<linearGradient id="${id}" x1="0" y1="0" x2="${x2}" y2="${y2}"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient>`;
const shadow = (cx, cy, rx, ry = 6, o = .18) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="#1b2742" opacity="${o}"/>`;
// 뭉게 모양 (원 여러 개)
const blob = (pts, fill) => pts.map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}"/>`).join('');

/* ===================== 꽃 언덕 ===================== */
// 풍차
sp('windmill', 120, 210, `
  ${shadow(60, 204, 40)}
  <path d="M38 200 L48 92 L72 92 L82 200Z" fill="#fff4e0"/><path d="M60 92 L72 92 L82 200 L60 200Z" fill="#ead6b6"/>
  <path d="M42 96 L60 70 L78 96Z" fill="#e8585c"/><path d="M60 70 L78 96 L60 96Z" fill="#c43e48"/>
  <path d="M52 200 L52 172 Q60 162 68 172 L68 200Z" fill="#8a5a3a"/>
  <circle cx="60" cy="128" r="7" fill="#7cc4ea" stroke="#5a3a24" stroke-width="2"/>
  <g transform="translate(60 84)">
    ${[0, 90, 180, 270].map(a => `<g transform="rotate(${a + 20})"><rect x="-4" y="-62" width="8" height="58" fill="#8a5a3a"/><rect x="4" y="-60" width="18" height="44" rx="2" fill="#ffffff" stroke="#cfc2ae" stroke-width="2"/><path d="M4 -46 H22 M4 -32 H22 M13 -60 V-16" stroke="#d8ccb8" stroke-width="1.5"/></g>`).join('')}
    <circle r="7" fill="#5a3a24"/><circle r="3" fill="#c49a6c"/>
  </g>`);
// 꽃집 (지붕 색 다른 두 가지)
const cottage = (name, roof, roofD, wall, wallD) => sp(name, 160, 140, `
  ${shadow(80, 134, 66)}
  <rect x="24" y="62" width="112" height="70" fill="${wall}"/><rect x="80" y="62" width="56" height="70" fill="${wallD}"/>
  <path d="M10 68 L80 14 L150 68Z" fill="${roof}"/><path d="M80 14 L150 68 L80 68Z" fill="${roofD}"/>
  <rect x="104" y="18" width="14" height="30" fill="#b9a48c"/><rect x="102" y="14" width="18" height="6" fill="#8a7660"/>
  <path d="M64 132 V100 Q80 86 96 100 V132Z" fill="#9a6440"/><circle cx="90" cy="116" r="2.5" fill="#ffd43b"/>
  <rect x="34" y="82" width="22" height="20" rx="3" fill="#bfe6ff" stroke="#fff" stroke-width="3"/>
  <rect x="106" y="82" width="22" height="20" rx="3" fill="#a9d6f2" stroke="#f1e6d6" stroke-width="3"/>
  <rect x="32" y="102" width="26" height="8" rx="3" fill="#7cc957"/>${blob([[37, 102, 4], [45, 101, 4], [53, 102, 4]], '#ff7aa8')}
  <rect x="104" y="102" width="26" height="8" rx="3" fill="#6bb84a"/>${blob([[109, 102, 4], [117, 101, 4], [125, 102, 4]], '#ffd43b')}`);
cottage('cottageRed', '#f06a6a', '#cc4b55', '#fff6e6', '#f0e2c8');
cottage('cottageBlue', '#5aa9e6', '#3f86c4', '#fff6e6', '#f0e2c8');
cottage('cottagePurple', '#a98bea', '#8466cf', '#fff6e6', '#f0e2c8');
// 꽃나무 (분홍/흰)
const blossom = (name, a, b, dot) => sp(name, 140, 196, `
  ${shadow(70, 190, 34)}
  <path d="M62 190 L64 120 L76 120 L78 190Z" fill="#a8693e"/><path d="M70 120 L76 120 L78 190 L70 190Z" fill="#8a5230"/>
  <path d="M66 140 L46 118 M74 132 L96 112" stroke="#a8693e" stroke-width="6" stroke-linecap="round"/>
  ${blob([[70, 66, 52], [36, 92, 34], [104, 92, 34], [52, 40, 30], [92, 44, 30]], a)}
  ${blob([[96, 82, 34], [104, 98, 28], [86, 114, 22]], b)}
  ${[[40, 70], [62, 36], [92, 56], [72, 92], [46, 104], [108, 80], [84, 30], [30, 94], [100, 108]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5" fill="${dot}"/><circle cx="${x}" cy="${y}" r="2" fill="#ffd43b"/>`).join('')}`);
blossom('blossomPink', '#ffb3cf', '#f48fb6', '#ffffff');
blossom('blossomWhite', '#ffffff', '#e8e4f4', '#ffb3cf');
blossom('blossomYellow', '#ffe58a', '#f5c84c', '#ffffff');
// 둥근 초록 나무
sp('treeRound', 120, 180, `
  ${shadow(60, 174, 30)}
  <path d="M53 174 L55 112 L65 112 L67 174Z" fill="#a8693e"/><path d="M60 112 L65 112 L67 174 L60 174Z" fill="#8a5230"/>
  ${blob([[60, 64, 46], [32, 88, 28], [88, 88, 28]], '#7ccf55')}${blob([[82, 76, 30], [90, 92, 24]], '#5fb840')}
  ${blob([[44, 50, 9], [70, 38, 7]], '#a6e27c')}<circle cx="78" cy="58" r="6" fill="#ff6b6b"/><circle cx="46" cy="84" r="6" fill="#ff6b6b"/><circle cx="66" cy="96" r="6" fill="#ff6b6b"/>`);
// 건초 더미
sp('hayBale', 110, 80, `${shadow(55, 76, 48)}<rect x="10" y="20" width="90" height="54" rx="12" fill="#f5cf5a"/><rect x="56" y="20" width="44" height="54" rx="12" fill="#e2b33e"/><path d="M18 32 H92 M16 48 H94 M18 62 H92" stroke="#d29c26" stroke-width="2.5"/><rect x="34" y="18" width="7" height="58" fill="#c0883a"/><rect x="70" y="18" width="7" height="58" fill="#a8742e"/>`);
// 꽃 무더기 (세 가지 색)
const flowers = (name, petal, petalD) => sp(name, 96, 56, `
  ${shadow(48, 52, 40, 5, .14)}
  ${blob([[18, 44, 14], [40, 40, 18], [64, 42, 16], [82, 46, 12]], '#6cc04a')}${blob([[60, 44, 14], [80, 48, 10]], '#55a83c')}
  ${[[20, 30], [38, 20], [56, 28], [74, 32], [46, 38], [30, 40], [66, 44]].map(([x, y], i) => `<g transform="translate(${x} ${y})">${[0, 72, 144, 216, 288].map(a => `<ellipse cx="0" cy="-5" rx="3.6" ry="5" fill="${i % 3 === 2 ? petalD : petal}" transform="rotate(${a})"/>`).join('')}<circle r="2.6" fill="#ffd43b"/></g>`).join('')}`);
flowers('flowersPink', '#ff8fb8', '#f06a9a');
flowers('flowersYellow', '#ffe066', '#f5c84c');
flowers('flowersBlue', '#8ec5ff', '#6aa6f0');
flowers('flowersWhite', '#ffffff', '#ece8f6');
// 튤립
const tulip = (name, c, d) => sp(name, 64, 84, `
  ${shadow(32, 80, 24, 4, .14)}
  ${[[16, 18], [32, 8], [48, 20]].map(([x, y]) => `<path d="M${x} 80 V${y + 22}" stroke="#4f9a34" stroke-width="3.5"/><path d="M${x} ${y + 52} q-12 -6 -12 -18 q10 2 12 12z" fill="#6cc04a"/><path d="M${x - 9} ${y + 8} q0 16 9 18 q9 -2 9 -18 l-4.5 6 l-4.5 -8 l-4.5 8z" fill="${c}"/><path d="M${x} ${y + 26} q9 -2 9 -18 l-4.5 6 l-4.5 -8z" fill="${d}"/>`).join('')}`);
tulip('tulipRed', '#ff6b6b', '#d9434f');
tulip('tulipYellow', '#ffd43b', '#e8a90c');
tulip('tulipPurple', '#b197fc', '#8a6ee8');
// 빨간 버섯
sp('mushroomRed', 70, 60, `${shadow(35, 56, 28, 4, .14)}<path d="M22 56 L24 34 L34 34 L36 56Z" fill="#fff4e6"/><path d="M42 56 L43 40 L51 40 L52 56Z" fill="#fff4e6"/><path d="M8 36 Q8 10 29 10 Q50 10 50 36Z" fill="#ff5c5c"/><path d="M29 10 Q50 10 50 36 L29 36Z" fill="#d93d48"/><circle cx="20" cy="24" r="4" fill="#fff"/><circle cx="34" cy="18" r="3" fill="#fff"/><circle cx="40" cy="28" r="3.5" fill="#fff"/><path d="M34 42 Q34 26 47 26 Q60 26 60 42Z" fill="#ff8a5c"/><circle cx="44" cy="34" r="2.5" fill="#fff"/><circle cx="52" cy="32" r="2.5" fill="#fff"/>`);
// 흰 울타리
sp('fenceWhite', 120, 56, `${shadow(60, 53, 56, 4, .14)}<rect x="4" y="22" width="112" height="7" fill="#f1ebe0"/><rect x="4" y="38" width="112" height="7" fill="#e2d9ca"/>${[10, 34, 58, 82, 106].map(x => `<path d="M${x - 6} 52 V14 L${x} 6 L${x + 6} 14 V52Z" fill="#ffffff"/><path d="M${x} 6 L${x + 6} 14 V52 H${x}Z" fill="#e8e0d2"/>`).join('')}`);
// 벌통
sp('beehive', 70, 90, `${shadow(35, 86, 26, 4)}<rect x="31" y="58" width="8" height="28" fill="#8a5a3a"/>${[[35, 58, 30, 12], [35, 44, 26, 12], [35, 30, 20, 11], [35, 18, 13, 9]].map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#f5c84c"/><path d="M${x} ${y - ry} A${rx} ${ry} 0 0 1 ${x} ${y + ry}Z" fill="#e2a930"/>`).join('')}<ellipse cx="35" cy="50" rx="6" ry="5" fill="#6a4020"/>`);

/* ===================== 푸른 바다 ===================== */
// 등대
sp('lighthouse', 96, 230, `
  ${shadow(48, 224, 40)}
  <path d="M22 222 L30 74 L66 74 L74 222Z" fill="#ffffff"/><path d="M48 74 L66 74 L74 222 L48 222Z" fill="#e6ecf4"/>
  <path d="M27.4 120 L68.6 120 L70.4 150 L25.6 150Z" fill="#f05a5a"/><path d="M48 120 L68.6 120 L70.4 150 L48 150Z" fill="#cc3e48"/>
  <path d="M24.8 172 L71.2 172 L73 202 L23 202Z" fill="#f05a5a"/><path d="M48 172 L71.2 172 L73 202 L48 202Z" fill="#cc3e48"/>
  <rect x="22" y="66" width="52" height="10" rx="2" fill="#3a4a66"/>
  <rect x="32" y="38" width="32" height="28" fill="#ffe680"/><path d="M32 38 H64 V66 H32Z M40 38 V66 M56 38 V66" fill="none" stroke="#3a4a66" stroke-width="3"/>
  <path d="M26 40 L48 16 L70 40Z" fill="#f05a5a"/><path d="M48 16 L70 40 L48 40Z" fill="#cc3e48"/><circle cx="48" cy="12" r="4" fill="#3a4a66"/>
  <path d="M41 222 V196 Q48 188 55 196 V222Z" fill="#5a6a86"/><rect x="42" y="92" width="12" height="16" rx="6" fill="#7cc4ea"/>`);
// 바닷가 오두막
const hut = (name, wall, wallD) => sp(name, 150, 140, `
  ${shadow(75, 136, 64)}
  <path d="M30 136 V118 M120 136 V118" stroke="#8a5a3a" stroke-width="6"/>
  <rect x="26" y="62" width="98" height="58" fill="${wall}"/><rect x="75" y="62" width="49" height="58" fill="${wallD}"/>
  ${[38, 52, 66, 80, 94, 108].map(x => `<path d="M${x} 62 V120" stroke="rgba(0,0,0,.08)" stroke-width="2"/>`).join('')}
  <path d="M8 68 L75 16 L142 68Z" fill="#f2c97a"/><path d="M75 16 L142 68 L75 68Z" fill="#d9a85a"/>
  ${[24, 40, 56].map(y => `<path d="M${75 - (y - 16) * 1.25} ${y} L${75 + (y - 16) * 1.25} ${y}" stroke="#c9944a" stroke-width="2"/>`).join('')}
  <rect x="60" y="84" width="30" height="36" fill="#7a4a2c"/><rect x="36" y="78" width="18" height="16" rx="2" fill="#bfe6ff" stroke="#fff" stroke-width="3"/>
  <rect x="98" y="78" width="18" height="16" rx="2" fill="#a9d6f2" stroke="#eee" stroke-width="3"/>
  <rect x="22" y="118" width="106" height="6" fill="#a8693e"/>`);
hut('beachHutBlue', '#7cc4ea', '#5aa9d6');
hut('beachHutPink', '#ff9fb8', '#f07c9c');
hut('beachHutMint', '#7ee0c0', '#55c4a2');
// 야자수 (직접 그림, 두 가지)
const palm = (name, lean, leaf, leafD) => sp(name, 160, 214, `
  ${shadow(80, 208, 30)}
  <path d="M74 208 Q${74 + lean} 136 ${80 + lean} 64" stroke="#b47a46" stroke-width="16" fill="none" stroke-linecap="round"/>
  ${[0,1,2,3,4,5,6,7,8].map(i=>{const t=i/9,y=208-(208-70)*t,x=74+lean*(1-(1-t)*(1-t))*1.0+6*t;return `<path d="M${(x-8).toFixed(1)} ${y.toFixed(1)} q8 4 16 0" stroke="#8f5a30" stroke-width="3" fill="none"/>`}).join('')}
  <g transform="translate(${80 + lean} 62)">
  ${[[-170,1],[-130,0],[-95,1],[-60,0],[-25,1],[10,0]].map(([a,k])=>`<g transform="rotate(${a})"><path d="M0 0 C22 -20 52 -18 76 6 C58 -2 44 0 34 8 C26 2 14 2 0 0Z" fill="${k?leaf:leafD}"/><path d="M4 0 C24 -12 48 -10 70 4" stroke="${k?leafD:leaf}" stroke-width="2" fill="none" opacity=".7"/></g>`).join('')}
  <circle cx="-7" cy="8" r="8" fill="#8a5a2a"/><circle cx="7" cy="9" r="8" fill="#6e4420"/><circle cx="0" cy="15" r="7" fill="#8a5a2a"/></g>`);
palm('palmA', 8, '#4fc06a', '#38a052');
palm('palmB', -6, '#5ccf7a', '#3fae5a');
// 파라솔
const umbrella = (name, a, b) => sp(name, 120, 120, `
  ${shadow(60, 116, 46, 6, .16)}
  <path d="M58 116 L62 44" stroke="#8a6a4a" stroke-width="4"/>
  <path d="M8 52 Q60 -6 112 52 Q99 44 86 52 Q73 44 60 52 Q47 44 34 52 Q21 44 8 52Z" fill="${a}"/>
  <path d="M34 52 Q47 44 60 52 L60 12 Q42 18 34 52Z" fill="${b}"/><path d="M86 52 Q99 44 112 52 Q104 26 82 15 Q88 30 86 52Z" fill="${b}"/>
  <circle cx="60" cy="12" r="4" fill="#fff"/>`);
umbrella('umbrellaRed', '#ff6b6b', '#ffffff');
umbrella('umbrellaBlue', '#4dabf7', '#ffffff');
umbrella('umbrellaYellow', '#ffd43b', '#ff922b');
// 모래성
sp('sandcastle', 110, 92, `${shadow(55, 88, 48, 5)}
  <path d="M14 88 V54 H96 V88Z" fill="#f2cf86"/><path d="M55 54 H96 V88 H55Z" fill="#dfb468"/>
  <path d="M30 54 V26 H50 V54Z M60 54 V30 H80 V54Z" fill="#f6d896"/><path d="M40 26 H50 V54 H40Z M70 30 H80 V54 H70Z" fill="#e0b870"/>
  ${[30, 36, 42].map(x => `<rect x="${x}" y="20" width="4" height="7" fill="#f6d896"/>`).join('')}${[60, 66, 72].map(x => `<rect x="${x}" y="24" width="4" height="7" fill="#f6d896"/>`).join('')}
  <path d="M40 20 V4" stroke="#8a6a4a" stroke-width="2"/><path d="M40 4 L54 9 L40 14Z" fill="#ff6b6b"/>
  <path d="M46 88 V72 Q55 64 64 72 V88Z" fill="#c9944a"/>${[14, 26, 38, 50, 62, 74, 86].map(x => `<rect x="${x}" y="48" width="8" height="7" fill="#f2cf86"/>`).join('')}`);
// 조개 · 불가사리 · 게 · 양동이
sp('shellPink', 60, 48, `${shadow(30, 45, 22, 3, .14)}<path d="M30 44 L6 26 Q8 6 30 4 Q52 6 54 26Z" fill="#ffb3c6"/><path d="M30 44 L30 4 Q52 6 54 26Z" fill="#f48fb1"/>${[-28, -14, 0, 14, 28].map(a => `<path d="M30 44 L${30 + a * .85} 8" stroke="#e07a9c" stroke-width="2"/>`).join('')}<path d="M22 44 h16 l-3 4 h-10z" fill="#f48fb1"/>`);
sp('shellWhite', 60, 48, `${shadow(30, 45, 22, 3, .14)}<path d="M30 44 L6 26 Q8 6 30 4 Q52 6 54 26Z" fill="#fff8ee"/><path d="M30 44 L30 4 Q52 6 54 26Z" fill="#efe2cf"/>${[-28, -14, 0, 14, 28].map(a => `<path d="M30 44 L${30 + a * .85} 8" stroke="#d8c6ac" stroke-width="2"/>`).join('')}<path d="M22 44 h16 l-3 4 h-10z" fill="#efe2cf"/>`);
const star5 = (cx, cy, R, r, rot = -90) => { let d = ''; for (let i = 0; i < 10; i++) { const a = (rot + i * 36) * Math.PI / 180, rr = i % 2 ? r : R; d += (i ? 'L' : 'M') + (cx + rr * Math.cos(a)).toFixed(1) + ' ' + (cy + rr * Math.sin(a)).toFixed(1); } return d + 'Z'; };
sp('starfishOrange', 60, 52, `${shadow(30, 48, 22, 3, .14)}<path d="${star5(30, 26, 26, 11)}" fill="#ff922b" stroke="#e8590c" stroke-width="3" stroke-linejoin="round"/>${[[30, 14], [22, 24], [38, 24], [30, 32], [25, 38], [35, 38]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="2" fill="#ffd8a8"/>`).join('')}`);
sp('starfishPink', 60, 52, `${shadow(30, 48, 22, 3, .14)}<path d="${star5(30, 26, 26, 11)}" fill="#f783ac" stroke="#d6336c" stroke-width="3" stroke-linejoin="round"/>${[[30, 14], [22, 24], [38, 24], [30, 32], [25, 38], [35, 38]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="2" fill="#ffdeeb"/>`).join('')}`);
sp('crab', 84, 58, `${shadow(42, 55, 32, 4, .16)}
  ${[0, 1, 2].map(i => `<path d="M${24 - i * 4} ${38 + i * 4} l-12 ${6 + i * 2}" stroke="#d6403f" stroke-width="4" stroke-linecap="round"/><path d="M${60 + i * 4} ${38 + i * 4} l12 ${6 + i * 2}" stroke="#d6403f" stroke-width="4" stroke-linecap="round"/>`).join('')}
  <path d="M22 30 L10 18 M62 30 L74 18" stroke="#d6403f" stroke-width="5" stroke-linecap="round"/>
  <path d="M2 10 Q10 0 18 8 Q12 10 10 18 Q2 18 2 10Z" fill="#ff6b6b"/><path d="M82 10 Q74 0 66 8 Q72 10 74 18 Q82 18 82 10Z" fill="#ff6b6b"/>
  <ellipse cx="42" cy="38" rx="24" ry="16" fill="#ff6b6b"/><path d="M42 22 A24 16 0 0 1 42 54Z" fill="#e8484c"/>
  <path d="M34 24 V14 M50 24 V14" stroke="#d6403f" stroke-width="3"/><circle cx="34" cy="12" r="5" fill="#fff"/><circle cx="50" cy="12" r="5" fill="#fff"/><circle cx="35" cy="12" r="2.5" fill="#1b2742"/><circle cx="51" cy="12" r="2.5" fill="#1b2742"/>
  <path d="M36 42 Q42 47 48 42" stroke="#9a2a2e" stroke-width="2.5" fill="none" stroke-linecap="round"/>`);
const bucket = (name, c, d) => sp(name, 64, 70, `${shadow(32, 67, 24, 3, .14)}<path d="M10 22 L16 66 H48 L54 22Z" fill="${c}"/><path d="M32 22 H54 L48 66 H32Z" fill="${d}"/><rect x="8" y="18" width="48" height="8" rx="3" fill="${d}"/><path d="M12 22 Q32 -8 52 22" stroke="#3a4a66" stroke-width="3" fill="none"/><path d="M50 30 L60 6" stroke="#ffd43b" stroke-width="5" stroke-linecap="round"/><path d="M56 6 l10 -4 l-4 10z" fill="#ffd43b"/>`);
bucket('bucketBlue', '#4dabf7', '#228be6');
bucket('bucketGreen', '#69db7c', '#40c057');
// 구명 튜브
sp('swimRing', 70, 50, `${shadow(35, 46, 30, 4, .14)}<ellipse cx="35" cy="28" rx="32" ry="18" fill="#ff6b6b"/><ellipse cx="35" cy="26" rx="14" ry="7" fill="#f2cf86"/>${[[-1, 1], [1, 1]].map(([s]) => `<path d="M${35 + s * 10} ${12} q${s * 8} 2 ${s * 14} 8 l${s * -4} 6 q${s * -6} -6 ${s * -12} -6z" fill="#ffffff"/>`).join('')}<path d="M10 36 q8 8 18 9 l1 -7 q-8 -1 -14 -6z" fill="#fff"/><path d="M60 36 q-8 8 -18 9 l-1 -7 q8 -1 14 -6z" fill="#fff"/>`);
// 갈매기 (하늘)
sp('gull', 70, 30, `<path d="M4 18 Q18 2 35 16 Q52 2 66 18 Q52 10 35 22 Q18 10 4 18Z" fill="#ffffff" stroke="#9aa6b8" stroke-width="2" stroke-linejoin="round"/><path d="M33 20 l4 0 l-2 4z" fill="#ffa94d"/>`);

/* ===================== 눈 덮인 산 ===================== */
// 눈 덮인 통나무집
const cabin = (name, wall, wallD) => sp(name, 160, 140, `
  ${shadow(80, 134, 66)}
  <rect x="24" y="64" width="112" height="68" fill="${wall}"/><rect x="80" y="64" width="56" height="68" fill="${wallD}"/>
  ${[74, 86, 98, 110, 122].map(y => `<path d="M24 ${y} H136" stroke="rgba(0,0,0,.14)" stroke-width="2"/>`).join('')}
  <path d="M8 72 L80 14 L152 72Z" fill="#6a4a3a"/><path d="M80 14 L152 72 L80 72Z" fill="#553a2c"/>
  <path d="M4 74 Q8 62 18 66 L80 14 L142 66 Q154 62 156 74 Q146 70 140 76 Q130 68 120 74 Q108 66 96 72 Q86 66 80 70 Q72 66 62 72 Q50 66 40 74 Q30 68 20 76 Q12 70 4 74Z" fill="#ffffff"/>
  <path d="M80 14 L60 30 Q72 34 80 28 Q88 34 100 30Z" fill="#ffffff"/>
  <rect x="106" y="20" width="14" height="30" fill="#9a8a7a"/><rect x="103" y="14" width="20" height="8" rx="3" fill="#ffffff"/>
  <path d="M64 132 V100 H96 V132Z" fill="#6a3e22"/><circle cx="90" cy="117" r="2.5" fill="#ffd43b"/>
  <rect x="34" y="86" width="22" height="20" rx="2" fill="#ffe08a" stroke="#fff" stroke-width="3"/><rect x="106" y="86" width="22" height="20" rx="2" fill="#f5cf6a" stroke="#eee" stroke-width="3"/>
  <path d="M30 108 Q45 102 60 108" stroke="#fff" stroke-width="5" stroke-linecap="round"/>`);
cabin('cabinRed', '#c0583e', '#a2462f');
cabin('cabinBrown', '#a8784e', '#8c603a');
cabin('cabinGreen', '#5f9a6a', '#4a8056');
// 이글루
sp('igloo', 140, 96, `${shadow(70, 92, 62, 5)}
  <path d="M8 90 A62 62 0 0 1 132 90Z" fill="#f4f9ff"/><path d="M70 28 A62 62 0 0 1 132 90 L70 90Z" fill="#dce8f6"/>
  ${[50, 66, 80].map((y, i) => `<path d="M${70 - Math.sqrt(62 * 62 - (90 - y) ** 2)} ${y} H${70 + Math.sqrt(62 * 62 - (90 - y) ** 2)}" stroke="#bfd2ea" stroke-width="2"/>`).join('')}
  ${[[40, 50], [90, 50], [60, 66], [100, 66], [30, 80], [74, 80]].map(([x, y]) => `<path d="M${x} ${y} V${y + 14}" stroke="#bfd2ea" stroke-width="2"/>`).join('')}
  <path d="M48 90 V72 Q70 50 92 72 V90Z" fill="#e8f1fb"/><path d="M56 90 V76 Q70 62 84 76 V90Z" fill="#3a4a66"/>`);
// 눈사람
const snowman = (name, scarf, hat) => sp(name, 80, 120, `${shadow(40, 116, 30, 5)}
  <circle cx="40" cy="88" r="28" fill="#ffffff"/><path d="M40 60 A28 28 0 0 1 40 116Z" fill="#e2ecf8"/>
  <circle cx="40" cy="46" r="20" fill="#ffffff"/><path d="M40 26 A20 20 0 0 1 40 66Z" fill="#e2ecf8"/>
  <path d="M20 22 H60 V27 H20Z" fill="${hat}"/><rect x="27" y="4" width="26" height="20" rx="2" fill="${hat}"/>
  <circle cx="33" cy="42" r="2.5" fill="#1b2742"/><circle cx="47" cy="42" r="2.5" fill="#1b2742"/><path d="M40 47 L56 51 L40 51Z" fill="#ff922b"/>
  <path d="M22 62 Q40 72 58 62 L58 68 Q40 78 22 68Z" fill="${scarf}"/><path d="M48 68 L52 84 L44 84 L42 70Z" fill="${scarf}"/>
  <circle cx="40" cy="82" r="3" fill="#1b2742"/><circle cx="40" cy="94" r="3" fill="#1b2742"/>
  <path d="M14 76 L-2 64 M66 76 L80 62" stroke="#8a5a3a" stroke-width="3.5" stroke-linecap="round"/>`);
snowman('snowmanRed', '#ff6b6b', '#3a4a66');
snowman('snowmanBlue', '#4dabf7', '#7a3b8e');
snowman('snowmanGreen', '#51cf66', '#3a4a66');
// 펭귄
sp('penguin', 60, 76, `${shadow(30, 73, 22, 4, .16)}
  <ellipse cx="30" cy="44" rx="20" ry="28" fill="#2b3550"/><ellipse cx="30" cy="48" rx="13" ry="21" fill="#ffffff"/>
  <path d="M10 40 Q2 52 8 60 Q14 52 14 44Z" fill="#1f2840"/><path d="M50 40 Q58 52 52 60 Q46 52 46 44Z" fill="#1f2840"/>
  <circle cx="24" cy="30" r="3" fill="#fff"/><circle cx="36" cy="30" r="3" fill="#fff"/><circle cx="24.5" cy="30.5" r="1.6" fill="#1b2742"/><circle cx="36.5" cy="30.5" r="1.6" fill="#1b2742"/>
  <path d="M26 36 L34 36 L30 42Z" fill="#ffa94d"/><ellipse cx="22" cy="72" rx="7" ry="3" fill="#ffa94d"/><ellipse cx="38" cy="72" rx="7" ry="3" fill="#ffa94d"/>
  <circle cx="20" cy="40" r="3" fill="#ffb3c6" opacity=".7"/><circle cx="40" cy="40" r="3" fill="#ffb3c6" opacity=".7"/>`);
// 눈 덮인 전나무 (직접 그림)
const pineSnow = (name, g, gd, h) => sp(name, 110, h, `${shadow(55, h - 6, 34)}
  <rect x="50" y="${h - 30}" width="10" height="24" fill="#8a5a3a"/>
  ${[0, 1, 2, 3].map(i => { const top = 6 + i * (h - 50) / 4, bot = top + (h - 50) / 4 + 22, w = 22 + i * 10; return `<path d="M55 ${top} L${55 - w} ${bot} L${55 + w} ${bot}Z" fill="${g}"/><path d="M55 ${top} L${55 + w} ${bot} L55 ${bot}Z" fill="${gd}"/><path d="M55 ${top} L${55 - w * .5} ${(top + bot) / 2} Q${55 - w * .2} ${(top + bot) / 2 + 6} 55 ${(top + bot) / 2 - 1} Q${55 + w * .2} ${(top + bot) / 2 + 6} ${55 + w * .5} ${(top + bot) / 2}Z" fill="#ffffff"/><path d="M${55 - w} ${bot} Q${55 - w * .5} ${bot - 6} 55 ${bot - 2} Q${55 + w * .5} ${bot - 6} ${55 + w} ${bot} Q55 ${bot + 3} ${55 - w} ${bot}Z" fill="#ffffff"/>`; }).join('')}`);
pineSnow('pineSnowA', '#2f9e6a', '#237a52', 190);
pineSnow('pineSnowB', '#3fae7a', '#2f8a5e', 170);
pineSnow('pineSnowC', '#5a8fb0', '#466f8c', 180);
// 썰매
sp('sled', 96, 50, `${shadow(48, 47, 40, 3, .14)}<path d="M8 40 H80 Q92 40 92 30" stroke="#9aa6b8" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M20 40 V30 M66 40 V30" stroke="#9aa6b8" stroke-width="4"/><rect x="10" y="20" width="70" height="12" rx="4" fill="#ff6b6b"/><rect x="45" y="20" width="35" height="12" rx="4" fill="#d9434f"/><rect x="14" y="10" width="40" height="12" rx="3" fill="#4dabf7"/><path d="M14 16 H54" stroke="#fff" stroke-width="2"/>`);
// 눈 덮인 덤불
sp('snowBush', 90, 52, `${shadow(45, 49, 38, 4, .14)}${blob([[20, 36, 16], [44, 28, 22], [68, 34, 18]], '#5aa36a')}${blob([[60, 32, 18], [72, 38, 12]], '#478a56')}${blob([[18, 24, 9], [32, 18, 10], [46, 12, 12], [60, 16, 10], [72, 22, 9]], '#ffffff')}`);
// 눈송이 결정
const crystal = (name, c, d) => sp(name, 50, 70, `${shadow(25, 67, 16, 3, .14)}<path d="M25 4 L40 26 L32 66 H18 L10 26Z" fill="${c}"/><path d="M25 4 L40 26 L32 66 H25Z" fill="${d}"/><path d="M25 4 L18 26 L25 66" stroke="#fff" stroke-width="2" opacity=".6" fill="none"/><path d="M8 44 L2 30 L8 20 L14 32Z" fill="${c}"/><path d="M42 50 L48 38 L46 28 L38 40Z" fill="${d}"/>`);
crystal('iceBlue', '#bfe3ff', '#8cc6f2');
crystal('icePurple', '#d9c8ff', '#b39af0');
// 장갑 · 눈덩이
sp('snowballs', 70, 44, `${shadow(35, 41, 30, 3, .14)}<circle cx="20" cy="30" r="12" fill="#fff"/><circle cx="44" cy="30" r="12" fill="#fff"/><circle cx="32" cy="14" r="11" fill="#fff"/><path d="M20 18 A12 12 0 0 1 20 42Z M44 18 A12 12 0 0 1 44 42Z M32 3 A11 11 0 0 1 32 25Z" fill="#dce8f6"/><circle cx="58" cy="36" r="7" fill="#fff"/><path d="M58 29 A7 7 0 0 1 58 43Z" fill="#dce8f6"/>`);
sp('skiSign', 60, 100, `${shadow(30, 97, 20, 3, .14)}<rect x="27" y="30" width="6" height="66" fill="#8a5a3a"/><path d="M6 14 H48 L56 24 L48 34 H6Z" fill="#ff922b"/><path d="M6 14 H30 V34 H6Z" fill="#ffa94d"/><path d="M14 24 H42" stroke="#fff" stroke-width="3" stroke-linecap="round"/><path d="M36 18 L42 24 L36 30" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M4 12 Q26 4 50 12" stroke="#fff" stroke-width="5" stroke-linecap="round"/>`);

/* ===================== 별빛 하늘 ===================== */
// 불 켜진 성
const castle = (name, wall, wallD, roof, roofD) => sp(name, 170, 190, `${shadow(85, 184, 72)}
  <rect x="20" y="70" width="34" height="112" fill="${wall}"/><rect x="37" y="70" width="17" height="112" fill="${wallD}"/>
  <rect x="116" y="70" width="34" height="112" fill="${wall}"/><rect x="133" y="70" width="17" height="112" fill="${wallD}"/>
  <rect x="44" y="100" width="82" height="82" fill="${wall}"/><rect x="85" y="100" width="41" height="82" fill="${wallD}"/>
  ${[44, 58, 72, 86, 100, 114].map(x => `<rect x="${x}" y="92" width="10" height="10" fill="${x > 84 ? wallD : wall}"/>`).join('')}
  <path d="M14 72 L37 22 L60 72Z" fill="${roof}"/><path d="M37 22 L60 72 L37 72Z" fill="${roofD}"/>
  <path d="M110 72 L133 22 L156 72Z" fill="${roof}"/><path d="M133 22 L156 72 L133 72Z" fill="${roofD}"/>
  <rect x="70" y="40" width="30" height="62" fill="${wall}"/><rect x="85" y="40" width="15" height="62" fill="${wallD}"/>
  <path d="M64 42 L85 2 L106 42Z" fill="${roof}"/><path d="M85 2 L106 42 L85 42Z" fill="${roofD}"/>
  <path d="M37 22 V8 M133 22 V8" stroke="#3a4a66" stroke-width="2"/><path d="M37 8 l12 4 l-12 4z M133 8 l12 4 l-12 4z" fill="#ffd43b"/>
  ${[[30, 100], [126, 100], [30, 136], [126, 136], [80, 60]].map(([x, y]) => `<rect x="${x}" y="${y}" width="14" height="20" rx="7" fill="#ffe066"/><rect x="${x + 2}" y="${y + 2}" width="10" height="16" rx="5" fill="#fff3bf"/>`).join('')}
  <path d="M70 182 V146 Q85 130 100 146 V182Z" fill="#4a3a6a"/><path d="M85 134 V182" stroke="#3a2a5a" stroke-width="2"/>`);
castle('castleLilac', '#e5dbff', '#c8b8f2', '#7950f2', '#5f3dc4');
castle('castleBlue', '#d0ebff', '#a8cef2', '#4c6ef5', '#364fc7');
castle('castlePink', '#ffe3ef', '#f5bfd6', '#e64980', '#c2255c');
// 천문대
sp('observatory', 140, 150, `${shadow(70, 144, 58)}
  <rect x="24" y="78" width="92" height="64" fill="#e9ecef"/><rect x="70" y="78" width="46" height="64" fill="#ced4da"/>
  <path d="M18 80 A52 52 0 0 1 122 80Z" fill="#dee2e6"/><path d="M70 28 A52 52 0 0 1 122 80 L70 80Z" fill="#adb5bd"/>
  <path d="M62 30 L78 30 L80 80 L60 80Z" fill="#495057"/>
  <path d="M66 48 L104 6" stroke="#868e96" stroke-width="12" stroke-linecap="round"/><path d="M66 48 L104 6" stroke="#adb5bd" stroke-width="6" stroke-linecap="round"/><circle cx="104" cy="6" r="5" fill="#ffe066"/>
  <path d="M58 142 V112 Q70 100 82 112 V142Z" fill="#5f3dc4"/><rect x="34" y="96" width="16" height="16" rx="8" fill="#ffe066"/><rect x="92" y="96" width="16" height="16" rx="8" fill="#f5cf4c"/>`);
// 가로등
const lamp = (name, glow) => sp(name, 50, 160, `${shadow(25, 156, 16, 3, .2)}
  <circle cx="25" cy="26" r="22" fill="${glow}" opacity=".35"/>
  <rect x="21" y="40" width="8" height="112" fill="#3a4a66"/><rect x="15" y="146" width="20" height="8" rx="2" fill="#2b3550"/>
  <path d="M12 40 H38 L34 14 H16Z" fill="${glow}"/><path d="M25 14 H34 L38 40 H25Z" fill="${glow}" opacity=".75"/><path d="M10 14 H40 L25 2Z" fill="#3a4a66"/><rect x="10" y="38" width="30" height="5" fill="#3a4a66"/>`);
lamp('lampYellow', '#ffe066');
lamp('lampBlue', '#a5d8ff');
// 보라 나무 (빛나는 열매)
const nightTree = (name, a, b, fruit) => sp(name, 120, 180, `${shadow(60, 174, 30, 6, .25)}
  <path d="M53 174 L55 110 L65 110 L67 174Z" fill="#6a4a7a"/><path d="M60 110 L65 110 L67 174 L60 174Z" fill="#553a66"/>
  ${blob([[60, 62, 46], [32, 88, 28], [88, 88, 28]], a)}${blob([[82, 74, 30], [90, 92, 24]], b)}
  ${[[40, 56], [72, 40], [84, 84], [48, 92], [64, 70], [28, 82]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="7" fill="${fruit}" opacity=".35"/><circle cx="${x}" cy="${y}" r="4" fill="${fruit}"/>`).join('')}`);
nightTree('treeNightPurple', '#9775fa', '#7048e8', '#fff3bf');
nightTree('treeNightTeal', '#3bc9db', '#1098ad', '#fff3bf');
// 빛나는 버섯
const glowMush = (name, c, d) => sp(name, 70, 64, `${shadow(35, 61, 28, 4, .2)}
  <ellipse cx="30" cy="22" rx="28" ry="18" fill="${c}" opacity=".25"/>
  <path d="M22 60 L24 34 L34 34 L36 60Z" fill="#f3f0ff"/><path d="M44 60 L45 42 L53 42 L54 60Z" fill="#f3f0ff"/>
  <path d="M8 36 Q8 10 29 10 Q50 10 50 36Z" fill="${c}"/><path d="M29 10 Q50 10 50 36 L29 36Z" fill="${d}"/>
  <path d="M36 44 Q36 28 49 28 Q62 28 62 44Z" fill="${c}"/><path d="M49 28 Q62 28 62 44 L49 44Z" fill="${d}"/>
  <circle cx="20" cy="24" r="3.5" fill="#fff" opacity=".85"/><circle cx="34" cy="17" r="2.5" fill="#fff" opacity=".85"/><circle cx="46" cy="36" r="2" fill="#fff" opacity=".85"/>`);
glowMush('glowMushBlue', '#74c0fc', '#4dabf7');
glowMush('glowMushPink', '#faa2c1', '#f06595');
glowMush('glowMushGreen', '#8ce99a', '#51cf66');
// 수정
const gem = (name, c, d, l) => sp(name, 64, 74, `${shadow(32, 71, 24, 3, .2)}
  <path d="M20 70 L14 34 L24 14 L34 34 L30 70Z" fill="${c}"/><path d="M24 14 L34 34 L30 70 L24 70Z" fill="${d}"/>
  <path d="M34 70 L32 26 L44 6 L56 26 L50 70Z" fill="${c}"/><path d="M44 6 L56 26 L50 70 L44 70Z" fill="${d}"/>
  <path d="M8 70 L6 50 L12 42 L18 50 L16 70Z" fill="${l}"/><path d="M38 30 L44 12" stroke="#fff" stroke-width="2.5" stroke-linecap="round" opacity=".8"/>`);
gem('gemPurple', '#b197fc', '#845ef7', '#d0bfff');
gem('gemBlue', '#74c0fc', '#339af0', '#a5d8ff');
gem('gemPink', '#f783ac', '#e64980', '#fcc2d7');
// 등불
const lantern = (name, c) => sp(name, 44, 70, `${shadow(22, 67, 14, 3, .2)}<circle cx="22" cy="36" r="20" fill="${c}" opacity=".3"/><path d="M22 4 V12" stroke="#3a4a66" stroke-width="2"/><rect x="12" y="12" width="20" height="5" rx="2" fill="#3a4a66"/><path d="M10 18 H34 Q38 36 34 54 H10 Q6 36 10 18Z" fill="${c}"/><path d="M22 18 H34 Q38 36 34 54 H22Z" fill="#000" opacity=".12"/><rect x="12" y="54" width="20" height="5" rx="2" fill="#3a4a66"/><path d="M18 59 v8 M26 59 v8" stroke="#3a4a66" stroke-width="2"/>`);
lantern('lanternOrange', '#ffa94d');
lantern('lanternPink', '#faa2c1');
// 밤 덤불
sp('bushNight', 90, 50, `${shadow(45, 47, 38, 4, .2)}${blob([[20, 34, 16], [44, 26, 22], [68, 32, 18]], '#5c4bb0')}${blob([[60, 30, 18], [72, 36, 12]], '#4a3b96')}${[[24, 26], [44, 16], [62, 24], [36, 34]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="2.5" fill="#fff3bf"/>`).join('')}`);
// 부엉이 기둥
sp('owlPost', 50, 110, `${shadow(25, 107, 16, 3, .2)}<rect x="19" y="50" width="12" height="56" fill="#6a4a3a"/><ellipse cx="25" cy="34" rx="18" ry="20" fill="#a0785a"/><ellipse cx="25" cy="40" rx="11" ry="12" fill="#e9d8c4"/><path d="M9 18 L14 26 M41 18 L36 26" stroke="#a0785a" stroke-width="6" stroke-linecap="round"/><circle cx="18" cy="28" r="7" fill="#fff"/><circle cx="32" cy="28" r="7" fill="#fff"/><circle cx="18" cy="28" r="3.5" fill="#1b2742"/><circle cx="32" cy="28" r="3.5" fill="#1b2742"/><path d="M22 34 L28 34 L25 39Z" fill="#ffa94d"/><path d="M16 52 h18" stroke="#ffa94d" stroke-width="4" stroke-linecap="round"/>`);
// 하늘: 초승달, 큰 별, 고리 행성, 작은 구름
sp('moonCrescent', 80, 80, `<circle cx="40" cy="40" r="36" fill="#fff3bf" opacity=".25"/><path d="M52 8 A32 32 0 1 0 72 56 A26 26 0 1 1 52 8Z" fill="#ffe066"/><circle cx="30" cy="36" r="4" fill="#f5c84c"/><circle cx="36" cy="54" r="3" fill="#f5c84c"/>`);
sp('starBig', 60, 60, `<circle cx="30" cy="30" r="26" fill="#ffe066" opacity=".22"/><path d="${star5(30, 31, 24, 11)}" fill="#ffe066" stroke="#f5c84c" stroke-width="2" stroke-linejoin="round"/><circle cx="24" cy="28" r="2" fill="#1b2742"/><circle cx="36" cy="28" r="2" fill="#1b2742"/><path d="M26 35 Q30 38 34 35" stroke="#1b2742" stroke-width="1.6" fill="none" stroke-linecap="round"/>`);
sp('starWish', 60, 60, `<circle cx="30" cy="30" r="24" fill="#a5d8ff" opacity=".25"/><path d="M30 4 L35 25 L56 30 L35 35 L30 56 L25 35 L4 30 L25 25Z" fill="#e7f5ff"/><path d="M30 4 L35 25 L56 30 L30 30Z" fill="#a5d8ff"/>`);
sp('planetRing', 100, 70, `<g transform="rotate(-14 50 36)"><path d="M6 36 A44 11 0 0 1 94 36" stroke="#ffd8a8" stroke-width="6" fill="none"/></g><circle cx="50" cy="35" r="24" fill="#ff922b"/><path d="M50 11 A24 24 0 0 1 50 59Z" fill="#e8590c"/><path d="M30 29 Q50 25 70 29 M28 41 Q50 37 72 41" stroke="#ffc078" stroke-width="3" fill="none"/><g transform="rotate(-14 50 36)"><path d="M94 36 A44 11 0 0 1 6 36" stroke="#ffd8a8" stroke-width="6" fill="none"/></g>`);
sp('planetSmall', 60, 60, `<circle cx="30" cy="30" r="22" fill="#63e6be"/><path d="M30 8 A22 22 0 0 1 30 52Z" fill="#20c997"/><circle cx="22" cy="24" r="4" fill="#96f2d7"/><circle cx="34" cy="38" r="5" fill="#38d9a9"/><circle cx="36" cy="18" r="2.5" fill="#96f2d7"/>`);
sp('cloudNight', 100, 50, `${blob([[24, 32, 16], [46, 22, 20], [70, 26, 18], [84, 34, 12]], '#6f63c9')}<rect x="10" y="32" width="80" height="16" rx="8" fill="#6f63c9"/>${blob([[40, 18, 9], [62, 20, 7]], '#8b80dc')}`);
// 꽃 언덕·바다 하늘: 나비, 연
sp('butterfly', 50, 40, `<path d="M25 20 Q8 0 4 12 Q2 24 25 22Z" fill="#ff8fb8"/><path d="M25 22 Q6 26 10 36 Q18 40 25 24Z" fill="#ffb3cf"/><path d="M25 20 Q42 0 46 12 Q48 24 25 22Z" fill="#f06a9a"/><path d="M25 22 Q44 26 40 36 Q32 40 25 24Z" fill="#ff8fb8"/><ellipse cx="25" cy="22" rx="2.5" ry="10" fill="#5a3a3a"/><path d="M24 12 Q20 4 16 4 M26 12 Q30 4 34 4" stroke="#5a3a3a" stroke-width="1.5" fill="none"/>`);
sp('kite', 60, 90, `<path d="M30 4 L52 30 L30 60 L8 30Z" fill="#ffd43b"/><path d="M30 4 L52 30 L30 30Z" fill="#ff922b"/><path d="M8 30 L30 60 L30 30Z" fill="#ff6b6b"/><path d="M30 60 Q22 70 32 76 Q40 82 30 88" stroke="#3a4a66" stroke-width="2" fill="none"/><path d="M26 70 l-6 -2 l2 6z M34 80 l6 -2 l-2 6z" fill="#4dabf7"/>`);
// 둥근 흰 구름 (낮 지역 공통)
const cloud = (name, pts, w, h) => sp(name, w, h, `<rect x="${pts[0][0]}" y="${h - 22}" width="${w - pts[0][0] * 2}" height="20" rx="10" fill="#e3f0fb"/>${blob(pts.map(([x,y,r])=>[x,y+3,r]), '#e3f0fb')}${blob(pts, '#ffffff')}<rect x="${pts[0][0]}" y="${h - 25}" width="${w - pts[0][0] * 2}" height="18" rx="9" fill="#ffffff"/>`);
cloud('puffA', [[24, 34, 18], [50, 24, 22], [76, 32, 16]], 100, 54);
cloud('puffB', [[22, 30, 14], [44, 22, 18], [66, 28, 14]], 88, 48);
cloud('puffC', [[26, 34, 18], [56, 22, 24], [86, 30, 18], [108, 36, 12]], 124, 56);

/* ===================== 배경 ===================== */
let _sd=7;const rnd=()=>{_sd=(_sd*16807)%2147483647;return _sd/2147483647};
const hills = (pts, fill) => `<path d="${pts}" fill="${fill}"/>`;
bg('flowerhill', `<defs>${lg('fs', '#bfe8ff', '#f1fbff')}${lg('fg', '#86d45c', '#5fb840')}</defs>
  <rect width="800" height="600" fill="url(#fs)"/>
  ${blob([[120, 250, 46], [170, 236, 58], [230, 254, 40], [560, 232, 52], [620, 216, 66], [690, 240, 46]], '#ffffff')}
  ${hills('M0 300 Q120 230 260 280 Q380 320 500 270 Q640 220 800 290 V600 H0Z', '#c3ecb0')}
  ${hills('M0 330 Q160 286 330 318 Q480 346 620 304 Q720 280 800 316 V600 H0Z', '#a3df7e')}
  ${[[90, 300], [170, 292], [420, 316], [560, 300], [690, 296], [740, 304]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="3" fill="${['#ff8fb8', '#ffe066', '#ffffff'][i % 3]}"/>`).join('')}
  <path d="M0 352 Q200 330 400 346 Q600 362 800 340 V600 H0Z" fill="url(#fg)"/>
  <path d="M0 352 Q200 330 400 346 Q600 362 800 340" stroke="#9ee27a" stroke-width="6" fill="none"/>
  <path d="M340 600 Q380 520 420 470 Q450 430 430 352 L470 352 Q500 440 470 490 Q440 540 470 600Z" fill="#e9d29a" opacity=".55"/>
  ${Array.from({ length: 70 }, (_, i) => { const x = (i * 137) % 800, y = 380 + ((i * 89) % 210); return `<circle cx="${x}" cy="${y}" r="${2 + i % 2}" fill="${['#ffb3cf', '#fff3a8', '#ffffff', '#c7e2ff'][i % 4]}" opacity=".9"/>`; }).join('')}`);
bg('beach', `<defs>${lg('bs', '#a9e3ff', '#e8f8ff')}${lg('bw', '#5cc8ef', '#2fa0d2')}${lg('bd', '#f8e2a8', '#efcb7e')}</defs>
  <rect width="800" height="600" fill="url(#bs)"/>
  ${blob([[110, 210, 34], [150, 196, 44], [200, 212, 30], [600, 180, 38], [650, 168, 48], [700, 186, 32]], '#ffffff')}
  <path d="M520 262 Q560 222 610 236 Q650 222 690 262Z" fill="#7cc48a"/><path d="M560 248 Q575 230 590 240" stroke="#5aa86a" stroke-width="4" fill="none"/>
  <rect y="258" width="800" height="100" fill="url(#bw)"/>
  ${[[60, 280], [240, 296], [420, 276], [610, 300], [730, 284], [150, 320], [520, 326], [340, 336]].map(([x, y]) => `<path d="M${x} ${y} q10 -6 20 0 q10 6 20 0" stroke="#ffffff" stroke-width="3" fill="none" opacity=".75" stroke-linecap="round"/>`).join('')}
  <g transform="translate(250 252)"><path d="M0 0 H50 L42 10 H8Z" fill="#ffffff"/><path d="M24 0 V-46" stroke="#8a6a4a" stroke-width="2.5"/><path d="M26 -44 L48 -4 H26Z" fill="#ff6b6b"/><path d="M22 -40 L6 -4 H22Z" fill="#ffffff"/></g>
  <g transform="translate(450 262) scale(.7)"><path d="M0 0 H50 L42 10 H8Z" fill="#ffffff"/><path d="M24 0 V-46" stroke="#8a6a4a" stroke-width="2.5"/><path d="M26 -44 L48 -4 H26Z" fill="#4dabf7"/><path d="M22 -40 L6 -4 H22Z" fill="#ffffff"/></g>
  <path d="M0 352 Q120 336 260 348 Q420 362 560 344 Q700 330 800 346 V600 H0Z" fill="url(#bd)"/>
  <path d="M0 352 Q120 336 260 348 Q420 362 560 344 Q700 330 800 346" stroke="#ffffff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".9"/>
  <path d="M0 364 Q120 348 260 360 Q420 374 560 356 Q700 342 800 358" stroke="#e8c27a" stroke-width="5" fill="none" opacity=".6"/>
  ${Array.from({ length: 40 }, (_, i) => { const x = (i * 151) % 800, y = 400 + ((i * 73) % 190); return `<circle cx="${x}" cy="${y}" r="2" fill="#d9b06a" opacity=".55"/>`; }).join('')}`);
bg('snowmount', `<defs>${lg('ss', '#bcd7ff', '#eef5ff')}${lg('sg', '#ffffff', '#e4eefa')}</defs>
  <rect width="800" height="600" fill="url(#ss)"/>
  ${blob([[640, 160, 36], [690, 148, 46], [740, 166, 30]], '#ffffff')}
  <path d="M-20 330 L120 150 L200 230 L320 90 L450 250 L540 170 L680 320Z" fill="#c8d8ef"/>
  <path d="M120 150 L200 230 L170 330 Z M320 90 L450 250 L400 330 Z M540 170 L680 320 L600 330Z" fill="#a9bfe0"/>
  <path d="M120 150 L94 184 L110 180 L122 196 L134 178 L150 186Z M320 90 L280 140 L302 134 L318 154 L338 132 L362 142Z M540 170 L510 208 L528 202 L542 218 L556 200 L572 206Z" fill="#ffffff"/>
  <path d="M380 330 L560 140 L700 290 L820 200 V330Z" fill="#dbe6f6"/><path d="M560 140 L700 290 L640 330Z M820 200 V330 L760 330Z" fill="#bccfea"/>
  <path d="M560 140 L528 176 L548 170 L562 188 L580 166 L598 174Z" fill="#ffffff"/>
  <path d="M0 340 Q200 312 400 332 Q600 352 800 326 V600 H0Z" fill="url(#sg)"/>
  <path d="M0 420 Q160 404 320 418 M460 470 Q600 452 780 468 M60 530 Q240 512 420 528" stroke="#d6e4f6" stroke-width="10" fill="none" stroke-linecap="round"/>
  ${Array.from({ length: 60 }, (_, i) => { const x = rnd() * 800, y = rnd() * 330; return `<circle cx="${x}" cy="${y}" r="${1.5 + i % 3 * .7}" fill="#ffffff" opacity=".9"/>`; }).join('')}`);
bg('nightsky', `<defs>${lg('ns', '#121a4a', '#4b4aa8')}${lg('ng', '#5b4bb0', '#3c2f86')}</defs>
  <rect width="800" height="600" fill="url(#ns)"/>
  <path d="M0 150 Q200 100 400 160 Q600 220 800 140" stroke="#63e6be" stroke-width="40" fill="none" opacity=".12" stroke-linecap="round"/>
  <path d="M0 190 Q220 150 420 200 Q620 250 800 180" stroke="#b197fc" stroke-width="30" fill="none" opacity=".12" stroke-linecap="round"/>
  ${Array.from({ length: 90 }, (_, i) => { const x = rnd() * 800, y = rnd() * 300; return `<circle cx="${x}" cy="${y}" r="${.8 + (i % 4) * .5}" fill="${i % 7 ? '#ffffff' : '#ffe066'}" opacity="${.5 + (i % 3) * .2}"/>`; }).join('')}
  ${hills('M0 316 Q140 262 300 300 Q440 334 560 290 Q690 250 800 300 V600 H0Z', '#3b2f7a')}
  ${[[90, 296], [130, 290], [610, 280], [650, 286]].map(([x, y]) => `<rect x="${x}" y="${y}" width="6" height="8" fill="#ffe066"/>`).join('')}
  <path d="M0 350 Q200 328 400 344 Q600 360 800 336 V600 H0Z" fill="url(#ng)"/>
  <path d="M0 350 Q200 328 400 344 Q600 360 800 336" stroke="#8b7ee6" stroke-width="5" fill="none"/>
  ${Array.from({ length: 30 }, (_, i) => { const x = (i * 149) % 800, y = 390 + ((i * 71) % 200); return `<circle cx="${x}" cy="${y}" r="2" fill="#b197fc" opacity=".55"/>`; }).join('')}`);

module.exports = { S, B };
