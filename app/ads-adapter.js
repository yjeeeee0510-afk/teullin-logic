// 구글 플레이 판 전용 광고 어댑터 (PLAY=1 로 앱 파일을 만들 때만 index.html에 들어간다).
// index.html의 ADS가 부르는 window.Capacitor.Plugins.RewardedAds.show({kind}) → {rewarded:boolean} 를
// @capacitor-community/admob 의 보상형 광고로 이어 준다. 끝까지 봐서 보상 이벤트가 온 때만 rewarded:true.
(function(){
  var CFG=/*ADS_CONFIG*/null;
  var C=window.Capacitor;if(!C||!C.Plugins||!CFG)return;
  var inited=false,busy=false;
  function admob(){return window.Capacitor&&window.Capacitor.Plugins&&window.Capacitor.Plugins.AdMob}   // 늦게 찾음(브리지가 준비된 뒤)
  function init(){
    var A=admob();if(!A)return Promise.reject(new Error('no AdMob'));
    if(inited)return Promise.resolve();
    return A.initialize({initializeForTesting:!!CFG.testing}).then(function(){inited=true});
  }
  function show(opt){
    var kind=(opt&&opt.kind)||'heart',id=CFG.rewarded[kind]||CFG.rewarded.heart;
    if(busy)return Promise.resolve({rewarded:false,error:'busy'});
    busy=true;
    return init().then(function(){
      var A=admob();
      return new Promise(function(resolve){
        var rewarded=false,done=false,subs=[];
        function finish(r){
          if(done)return;done=true;busy=false;
          subs.forEach(function(s){try{s.remove()}catch(e){}});
          resolve({rewarded:r});
        }
        function on(ev,fn){return A.addListener(ev,fn).then(function(h){subs.push(h)})}
        Promise.all([
          on('onRewardedVideoAdReward',function(){rewarded=true}),
          on('onRewardedVideoAdDismissed',function(){finish(rewarded)}),
          on('onRewardedVideoAdFailedToLoad',function(){finish(false)}),
          on('onRewardedVideoAdFailedToShow',function(){finish(false)})
        ]).then(function(){
          return A.prepareRewardVideoAd({adId:id,isTesting:!!CFG.testing});
        }).then(function(){
          return A.showRewardVideoAd();
        }).catch(function(){finish(false)});
        setTimeout(function(){finish(rewarded)},180000);   // 3분 안에 안 끝나면 정리(보상은 받았을 때만)
      });
    }).catch(function(){busy=false;return {rewarded:false}});
  }
  C.Plugins.RewardedAds={show:show};
})();
