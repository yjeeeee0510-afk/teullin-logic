// [초안 · 미배포 · 미검증] Google Play 영수증을 검증하고 구매를 서버에 기록하는 Supabase Edge Function.
// 결제를 켜는 날(프로모션 때)에 대표가 배포한다. 지금은 아무 데서도 호출하지 않는다.
//
// 필요한 것(켜는 날):
//  1) Play Console → 설정 → API 액세스에서 구글 서비스 계정 연결(앱 결제 권한)
//  2) 서비스 계정 JSON을 Supabase 함수 비밀로 저장:  supabase secrets set GOOGLE_SERVICE_ACCOUNT_JSON='...'  (채팅·저장소에 쓰지 않는다)
//  3) supabase functions deploy verify-purchase
//  4) SQL: app_flags 'payments' 와 products.active 를 켠다 (patch-7.0-payments.sql 머리말 참고)
//
// 흐름: 앱 → (로그인 토큰 + productId + purchaseToken) → 이 함수 → Play 검증 → grant_purchase(service_role) → 앱이 pay_pending/pay_claim 으로 받아 감
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const PACKAGE = 'com.jungdok.teullinlogic';
const SERVICE_ACCOUNT = JSON.parse(Deno.env.get('GOOGLE_SERVICE_ACCOUNT_JSON') ?? '{}');

async function googleToken(): Promise<string> {
  // 서비스 계정 JWT → 액세스 토큰 (androidpublisher 범위)
  const enc = (o: unknown) => btoa(JSON.stringify(o)).replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
  const now = Math.floor(Date.now() / 1000);
  const head = enc({ alg: 'RS256', typ: 'JWT' });
  const claim = enc({ iss: SERVICE_ACCOUNT.client_email, scope: 'https://www.googleapis.com/auth/androidpublisher', aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600 });
  const pem = SERVICE_ACCOUNT.private_key.replace(/-----[^-]+-----/g, '').replace(/\s+/g, '');
  const key = await crypto.subtle.importKey('pkcs8', Uint8Array.from(atob(pem), (c) => c.charCodeAt(0)), { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
  const sig = new Uint8Array(await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(`${head}.${claim}`)));
  const jws = `${head}.${claim}.${btoa(String.fromCharCode(...sig)).replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_')}`;
  const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion: jws }) });
  if (!r.ok) throw new Error('google-token');
  return (await r.json()).access_token;
}

Deno.serve(async (req) => {
  const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { 'Content-Type': 'application/json' } });
  try {
    // 1) 누가 요청했는지: 앱이 보낸 로그인 토큰으로 확인 (게스트는 거절)
    const url = Deno.env.get('SUPABASE_URL')!;
    const admin = createClient(url, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
    const jwt = (req.headers.get('Authorization') ?? '').replace('Bearer ', '');
    const { data: u } = await admin.auth.getUser(jwt);
    if (!u?.user || u.user.is_anonymous) return json({ ok: false, reason: 'login' }, 401);

    const { productId, purchaseToken } = await req.json();
    if (typeof productId !== 'string' || typeof purchaseToken !== 'string' || purchaseToken.length > 600) return json({ ok: false, reason: 'input' }, 400);

    // 2) Google Play 에 이 구매가 진짜인지 확인 (구매 완료 상태 = 0)
    const access = await googleToken();
    const g = await fetch(`https://androidpublisher.googleapis.com/androidpublisher/v3/applications/${PACKAGE}/purchases/products/${encodeURIComponent(productId)}/tokens/${encodeURIComponent(purchaseToken)}`, { headers: { Authorization: `Bearer ${access}` } });
    if (!g.ok) return json({ ok: false, reason: 'google' }, 402);
    const p = await g.json();
    if (p.purchaseState !== 0) return json({ ok: false, reason: 'state' }, 402);

    // 3) 서버에 기록 (스위치·상품·중복·첫 구매 규칙은 SQL 함수가 지킨다)
    const { data, error } = await admin.rpc('grant_purchase', { p_user: u.user.id, p_product: productId, p_token: purchaseToken, p_order: p.orderId ?? null });
    if (error) return json({ ok: false, reason: 'server' }, 500);
    if (!data?.ok) return json(data, 409);

    // 4) Google 에 구매 확인(acknowledge) — 3일 안에 안 하면 자동 환불된다. 소비형 상품은 consume 으로 다시 살 수 있게 한다.
    await fetch(`https://androidpublisher.googleapis.com/androidpublisher/v3/applications/${PACKAGE}/purchases/products/${encodeURIComponent(productId)}/tokens/${encodeURIComponent(purchaseToken)}:acknowledge`, { method: 'POST', headers: { Authorization: `Bearer ${access}`, 'Content-Type': 'application/json' }, body: '{}' });
    return json({ ok: true });
  } catch (_e) {
    return json({ ok: false, reason: 'error' }, 500);
  }
});
