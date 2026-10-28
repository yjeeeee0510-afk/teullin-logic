// OpenAI 이미지 API로 게임 그림을 만든다. (Node 18 이상, 추가 설치 없음)
//
// 준비: OpenAI API 키를 환경 변수 OPENAI_API_KEY 에 넣는다. 키를 이 파일이나 저장소에 적지 않는다.
//   Windows PowerShell:  setx OPENAI_API_KEY "sk-..."   (새 터미널부터 적용)
//   macOS/Linux:         export OPENAI_API_KEY="sk-..."
//
// 사용 예:
//   node tools/ai_art/generate.mjs --dry                 # 요청 목록과 예상 장수만 보기 (요금 없음)
//   node tools/ai_art/generate.mjs --zone "꽃 언덕"       # 꽃 언덕 그림만 만들기
//   node tools/ai_art/generate.mjs --only windmill,crab  # 이름을 골라 만들기
//   node tools/ai_art/generate.mjs                       # 90장 전부 (이미 만든 건 건너뜀)
//   옵션: --force (이미 만든 것도 다시), --quality low|medium|high (기본 medium)
//
// 결과: tools/ai_art/out/raw/<이름>.png  → 다음 단계: python3 tools/ai_art/process.py
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'out', 'raw');
const API = 'https://api.openai.com/v1/images';
const MODEL = process.env.OPENAI_IMAGE_MODEL || 'gpt-image-1';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true) : d; };
const DRY = !!opt('--dry', false), FORCE = !!opt('--force', false), QUALITY = opt('--quality', 'medium');
const ONLY = opt('--only', '') ? String(opt('--only')).split(',').map(s => s.trim()) : null;
const ZONE = opt('--zone', '') || null;

const spec = JSON.parse(fs.readFileSync(path.join(DIR, 'items.json'), 'utf8'));
let items = spec.items;
if (ZONE) items = items.filter(i => i.zone === ZONE);
if (ONLY) {
  // 색 변형을 고르면 바탕이 되는 그림도 같이 필요하다
  const want = new Set(ONLY);
  for (const i of spec.items) if (want.has(i.name) && i.variantOf) want.add(i.variantOf);
  items = spec.items.filter(i => want.has(i.name));
}
// 바탕 그림을 먼저, 색 변형은 그 뒤에
items.sort((a, b) => (a.variantOf ? 1 : 0) - (b.variantOf ? 1 : 0));

const key = process.env.OPENAI_API_KEY;
if (!DRY && !key) { console.error('OPENAI_API_KEY 환경 변수가 없어요. 위 안내대로 키를 넣고 새 터미널에서 다시 실행해 주세요.'); process.exit(1); }
fs.mkdirSync(OUT, { recursive: true });

const fullPrompt = i => [spec.style, i.type === 'scene' ? spec.scene : spec.sprite, i.prompt].join('\n');
const sizeOf = i => (i.type === 'scene' ? '1536x1024' : '1024x1024');
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function call(url, init, tries = 4) {
  for (let t = 1; ; t++) {
    const r = await fetch(url, init);
    if (r.ok) return r.json();
    const body = await r.text();
    if ((r.status === 429 || r.status >= 500) && t < tries) { await sleep(5000 * t); continue; }
    throw new Error(`${r.status} ${body.slice(0, 300)}`);
  }
}

async function generate(i) {
  const body = { model: MODEL, prompt: fullPrompt(i), size: sizeOf(i), quality: QUALITY, n: 1, output_format: 'png' };
  if (i.type !== 'scene') body.background = 'transparent';
  const j = await call(`${API}/generations`, { method: 'POST', headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  return Buffer.from(j.data[0].b64_json, 'base64');
}

async function editFrom(i) {
  // 같은 모양에 색만 바꾸기: 바탕 그림을 넣고 수정 요청
  const basePath = path.join(OUT, `${i.variantOf}.png`);
  if (!fs.existsSync(basePath)) throw new Error(`바탕 그림 ${i.variantOf}.png 가 아직 없어요`);
  const fd = new FormData();
  fd.append('model', MODEL);
  fd.append('image', new Blob([fs.readFileSync(basePath)], { type: 'image/png' }), `${i.variantOf}.png`);
  fd.append('prompt', `${spec.style}\n${spec.sprite}\n${i.prompt}`);
  fd.append('size', sizeOf(i));
  fd.append('quality', QUALITY);
  fd.append('background', 'transparent');
  fd.append('output_format', 'png');
  const j = await call(`${API}/edits`, { method: 'POST', headers: { Authorization: `Bearer ${key}` }, body: fd });
  return Buffer.from(j.data[0].b64_json, 'base64');
}

const todo = items.filter(i => FORCE || !fs.existsSync(path.join(OUT, `${i.name}.png`)));
console.log(`모델 ${MODEL}, 품질 ${QUALITY} · 만들 그림 ${todo.length}장 (전체 ${items.length}장 중, 이미 있는 건 건너뜀)`);
if (DRY) { for (const i of todo) console.log(`- ${i.name} [${i.zone}] ${i.variantOf ? `(${i.variantOf} 색 변형) ` : ''}${i.prompt}`); process.exit(0); }

let ok = 0; const failed = [];
for (const i of todo) {
  process.stdout.write(`${i.name} … `);
  try {
    const png = i.variantOf ? await editFrom(i) : await generate(i);
    fs.writeFileSync(path.join(OUT, `${i.name}.png`), png);
    ok++; console.log('완료');
  } catch (e) { failed.push(i.name); console.log(`실패: ${e.message}`); }
}
console.log(`\n완료 ${ok}장${failed.length ? `, 실패 ${failed.length}장: ${failed.join(',')}  → --only ${failed.join(',')} 로 다시 시도` : ''}`);
console.log('다음 단계: python3 tools/ai_art/process.py');
