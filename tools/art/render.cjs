const {chromium}=require('playwright');
const fs=require('fs');const path=require('path');
delete require.cache[require.resolve('./art.cjs')];
const {S,B}=require('./art.cjs');
const out=process.argv[2];fs.mkdirSync(out+'/sprites',{recursive:true});fs.mkdirSync(out+'/scenes',{recursive:true});
(async()=>{const b=await chromium.launch();
 const p2=await (await b.newContext({deviceScaleFactor:2})).newPage();
 for(const [n,s] of Object.entries(S)){await p2.setContent(`<body style="margin:0;background:transparent">${s.svg}</body>`);const el=await p2.$('svg');await el.screenshot({path:`${out}/sprites/${n}.png`,omitBackground:true});}
 const p1=await (await b.newContext({deviceScaleFactor:1})).newPage();
 for(const [n,s] of Object.entries(B)){await p1.setContent(`<body style="margin:0">${s}</body>`);const el=await p1.$('svg');await el.screenshot({path:`${out}/scenes/${n}.png`});}
 console.log(Object.keys(S).length,'sprites',Object.keys(B).length,'scenes');await b.close();})();
