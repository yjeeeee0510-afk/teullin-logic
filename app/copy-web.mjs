// 게임 웹 파일(저장소 루트)을 앱 안에 넣을 www/로 복사. 앱에는 개발용 원본(art-src·tools 등)은 넣지 않는다.
import {cpSync,rmSync,mkdirSync,existsSync} from 'node:fs';
const R='..',W='www';
rmSync(W,{recursive:true,force:true});mkdirSync(W);
for(const f of ['index.html','rank-config.js','manifest.webmanifest','icons','img','sfx'])
  if(existsSync(`${R}/${f}`))cpSync(`${R}/${f}`,`${W}/${f}`,{recursive:true});
console.log('www 준비 완료');
