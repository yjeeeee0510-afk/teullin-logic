// 구글 플레이 판 전용 광고 어댑터 (PLAY=1 로 앱 파일을 만들 때만 index.html에 들어간다).
// index.html의 ADS가 부르는 window.Capacitor.Plugins.RewardedAds.show({kind}) → {rewarded:boolean} 를
// @capacitor-community/admob 의 보상형 광고로 이어 준다. 끝까지 봐서 보상 이벤트가 온 때만 rewarded:true.
(function(){
  var CFG=/*ADS_CONFIG*/null;
  var C=window.Capacitor;if(!C||!C.Plugins||!CFG)return;
  var inited=false,busy=false;
  // 이 앱은 번들러가 없어 플러그인의 JS가 안 불려서 Capacitor.Plugins.AdMob이 비어 있다(7.6 실기기 확인: '초기화' 단계 실패).
  // 그래서 registerPlugin('AdMob')으로 직접 등록해 쓴다(안드로이드에 AdMob 네이티브가 있으면 그대로 연결됨).
  var proxy=null;
  function admob(){
    var Cp=window.Capacitor;if(!Cp)return null;
    if(Cp.Plugins&&Cp.Plugins.AdMob)return Cp.Plugins.AdMob;
    if(proxy)return proxy;
    if(typeof Cp.registerPlugin==='function'){try{proxy=Cp.registerPlugin('AdMob')}catch(e){proxy=null}}
    return proxy;
  }
  function msg(e){try{if(!e)return '';if(typeof e==='string')return e.slice(0,80);var m=e.message||e.errorMessage||'';var c=(e.code!==undefined?e.code:(e.errorCode!==undefined?e.errorCode:''));return String(c!==''?(c+' '+m):m).slice(0,80)}catch(x){return ''}}
  function init(){
    var A=admob();if(!A)return Promise.reject(new Error('no AdMob'));
    if(inited)return Promise.resolve();
    return Promise.resolve(A.initialize({initializeForTesting:!!CFG.testing})).then(function(){inited=true});
  }
  function show(opt){
    var kind=(opt&&opt.kind)||'heart',id=CFG.rewarded[kind]||CFG.rewarded.heart;
    if(busy)return Promise.resolve({rewarded:false,error:'busy'});
    busy=true;
    return init().catch(function(e){busy=false;throw {stage:'초기화',msg:msg(e)}}).then(function(){
      var A=admob();
      return new Promise(function(resolve){
        var rewarded=false,done=false,subs=[],stage='준비';
        function finish(r,why,m){
          if(done)return;done=true;busy=false;
          subs.forEach(function(s){try{s.remove()}catch(e){}});
          resolve(r?{rewarded:true}:{rewarded:false,stage:why||stage,msg:m||''});
        }
        function on(ev,fn){return Promise.resolve(A.addListener(ev,fn)).then(function(h){if(h)subs.push(h)})}
        Promise.all([
          on('onRewardedVideoAdReward',function(){rewarded=true}),
          on('onRewardedVideoAdDismissed',function(){finish(rewarded,'시청 중단')}),
          on('onRewardedVideoAdFailedToLoad',function(e){finish(false,'불러오기',msg(e))}),
          on('onRewardedVideoAdFailedToShow',function(e){finish(false,'표시',msg(e))})
        ]).then(function(){
          stage='불러오기';return A.prepareRewardVideoAd({adId:id,isTesting:!!CFG.testing});
        }).then(function(){
          stage='표시';return A.showRewardVideoAd();
        }).catch(function(e){finish(false,stage,msg(e))});
        setTimeout(function(){finish(rewarded,'시간 초과')},180000);   // 3분 안에 안 끝나면 정리(보상은 받았을 때만)
      });
    }).catch(function(e){busy=false;return {rewarded:false,stage:(e&&e.stage)||'초기화',msg:(e&&e.msg)||msg(e)}});
  }
  C.Plugins.RewardedAds={show:show};
})();
