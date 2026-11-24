// 게임 웹 파일(저장소 루트)을 앱 안에 넣을 www/로 복사. 앱에는 개발용 원본(art-src·tools 등)은 넣지 않는다.
// PLAY=1 이면 구글 플레이 판 표시(window.__PLAY_STORE=true)를 넣어 자체 업데이트 안내를 끈다.
import {cpSync,rmSync,mkdirSync,existsSync,readFileSync,writeFileSync} from 'node:fs';
const R='..',W='www';
rmSync(W,{recursive:true,force:true});mkdirSync(W);
for(const f of ['index.html','rank-config.js','manifest.webmanifest','icons','img','sfx'])
  if(existsSync(`${R}/${f}`))cpSync(`${R}/${f}`,`${W}/${f}`,{recursive:true});
if(process.env.PLAY){
  const p=`${W}/index.html`;let h=readFileSync(p,'utf8');
  h=h.replace('<head>','<head><script>window.__PLAY_STORE=true</script>');
  // 구글 플레이 판에만 보상형 광고 어댑터(ads-adapter.js + ads-config.json)를 넣는다. 사이드로드·웹에는 안 들어간다.
  const cfg=JSON.parse(readFileSync('ads-config.json','utf8'));delete cfg._설명;
  const ad=readFileSync('ads-adapter.js','utf8').replace('/*ADS_CONFIG*/null',JSON.stringify(cfg));
  h=h.replace('<head>','<head><script>'+ad+'</script>');
  console.log('광고 어댑터 포함',cfg.testing?'(테스트 광고 ID)':'(출시용 광고 ID)');
  writeFileSync(p,h);
  console.log('www 준비 완료 (구글 플레이 판)');
}else console.log('www 준비 완료');
