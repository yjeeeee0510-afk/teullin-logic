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
  writeFileSync(p,h);
  console.log('www 준비 완료 (구글 플레이 판)');
}else console.log('www 준비 완료');
