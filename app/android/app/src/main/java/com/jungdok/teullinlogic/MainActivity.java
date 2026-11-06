package com.jungdok.teullinlogic;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        // 구글 플레이 판(play 플레이버)에서는 자체 설치 기능을 쓰지 않는다 → 플러그인 미등록
        if (!BuildConfig.PLAY_STORE) {
            registerPlugin(ApkUpdatePlugin.class);
        }
        super.onCreate(savedInstanceState);
    }
}
