-- 2026-11-14 · 패치 7.0 결제 뼈대 + 기능 스위치 (대표가 SQL Editor에서 직접 실행)
-- 결제는 프로모션 때 켠다(D-012): 스위치(app_flags)와 상품(products.active)이 모두 꺼진 채로 들어간다.
-- 실행하지 않아도 게임은 정상 동작한다(특별 상점은 '준비 중'으로만 보임).
--
-- 켜는 날 할 일(대표): ① Play 판매자 등록·상품 등록 ② 구글 서비스 계정 연결 ③ supabase/functions/verify-purchase 배포
--                      ④ 아래 두 줄로 스위치와 상품을 켠다
--   update public.app_flags set enabled = true where key = 'payments';
--   update public.products set active = true where id in ('coins_s','coins_m','coins_l', ...);

-- 기능 스위치 (결제·광고 공용)
create table if not exists public.app_flags (
  key text primary key,
  enabled boolean not null default false,
  updated_at timestamptz not null default now()
);
insert into public.app_flags (key, enabled) values ('payments', false), ('ads', false) on conflict (key) do nothing;
alter table public.app_flags enable row level security;
revoke all on public.app_flags from anon, authenticated;

-- 상품: 무엇을 주는지는 서버가 정한다(앱이 정한 값은 믿지 않는다). 가격은 Play Console 상품에 있다.
-- grant 예: {"coins":1000,"hints":5,"hearts":5,"cookies":0,"own":["bg.candy","base.cloud"]}
create table if not exists public.products (
  id text primary key,
  title text not null,
  grant_data jsonb not null,
  first_only boolean not null default false,       -- 스타터 팩처럼 계정당 한 번만
  active boolean not null default false,           -- 꺼져 있으면 스위치가 켜져도 지급 안 됨
  created_at timestamptz not null default now()
);
alter table public.products enable row level security;
revoke all on public.products from anon, authenticated;

-- 제안 상품(모두 꺼짐). 수량·구성은 켜기 전에 정한다.
insert into public.products (id, title, grant_data, first_only) values
 ('coins_s', '코인 묶음 S', '{"coins":1000}', false),
 ('coins_m', '코인 묶음 M', '{"coins":3000}', false),
 ('coins_l', '코인 묶음 L', '{"coins":8000}', false),
 ('pack_bg', '배경 패키지', '{"own":["bg.candy","bg.flower","bg.sea","bg.snow","bg.night","bg.dots","bg.sunset","bg.aurora","bg.gold"]}', false),
 ('pack_base', '받침 패키지', '{"own":["base.cloud","base.grass","base.stump","base.ice","base.cookie","base.macaron","base.gem","base.stars","base.throne"]}', false),
 ('pack_comp', '동행 패키지', '{"own":["comp.0","comp.1","comp.2","comp.3","comp.4","comp.5","comp.6","comp.7","comp.8","comp.9","comp.10","comp.11"]}', false),
 ('starter', '스타터 팩', '{"coins":1000,"hints":5,"hearts":5,"own":["bg.candy","base.cloud"]}', true)
on conflict (id) do nothing;

-- 구매 기록: 같은 구매 토큰은 한 번만, 스타터 팩 같은 첫 구매 상품은 계정당 한 번만
create table if not exists public.purchases (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  product_id text not null references public.products(id),
  token text not null unique,
  order_id text,
  grant_data jsonb not null,                       -- 구매 당시 지급 내용(나중에 상품이 바뀌어도 그대로)
  created_at timestamptz not null default now(),
  applied_at timestamptz                           -- 앱이 받아 간 시각(한 번만 받아 감)
);
create index if not exists purchases_user_idx on public.purchases(user_id);
create unique index if not exists purchases_first_only_idx on public.purchases(user_id, product_id)
  where product_id = 'starter';
alter table public.purchases enable row level security;
revoke all on public.purchases from anon, authenticated;

-- 누구나(게스트 포함) 스위치를 읽는다
create or replace function public.app_flags()
returns table (key text, enabled boolean)
language sql stable security definer set search_path = public as $$
  select f.key, f.enabled from public.app_flags f;
$$;

-- 서버 전용(검증 서버 함수가 service_role로 호출): 영수증 검증이 끝난 구매를 기록한다
create or replace function public.grant_purchase(p_user uuid, p_product text, p_token text, p_order text)
returns json language plpgsql security definer set search_path = public as $$
declare pr public.products; pid uuid;
begin
  if not exists (select 1 from public.app_flags where key = 'payments' and enabled) then
    return json_build_object('ok', false, 'reason', 'off');
  end if;
  select * into pr from public.products where id = p_product and active;
  if not found then return json_build_object('ok', false, 'reason', 'product'); end if;
  if exists (select 1 from public.purchases where token = p_token) then
    return json_build_object('ok', true, 'reason', 'duplicate');          -- 같은 구매를 다시 보내도 한 번만
  end if;
  if pr.first_only and exists (select 1 from public.purchases where user_id = p_user and product_id = p_product) then
    return json_build_object('ok', false, 'reason', 'first_only');
  end if;
  insert into public.purchases (user_id, product_id, token, order_id, grant_data)
  values (p_user, p_product, p_token, p_order, pr.grant_data) returning id into pid;
  return json_build_object('ok', true, 'id', pid);
end $$;

-- 앱: 아직 받아 가지 않은 구매
create or replace function public.pay_pending()
returns table (id uuid, product_id text, created_at timestamptz)
language sql stable security definer set search_path = public as $$
  select p.id, p.product_id, p.created_at from public.purchases p
  where p.user_id = auth.uid() and p.applied_at is null
    and coalesce((auth.jwt() ->> 'is_anonymous')::boolean, false) = false
  order by p.created_at;
$$;

-- 앱: 받아 가기 (서버 기록으로 딱 한 번만 지급 내용을 돌려준다)
create or replace function public.pay_claim(p_id uuid)
returns json language plpgsql security definer set search_path = public as $$
declare g jsonb;
begin
  if auth.uid() is null or coalesce((auth.jwt() ->> 'is_anonymous')::boolean, false) then
    return json_build_object('ok', false, 'reason', 'guest');
  end if;
  update public.purchases set applied_at = now()
   where id = p_id and user_id = auth.uid() and applied_at is null
   returning grant_data into g;
  if not found then return json_build_object('ok', false, 'reason', 'already'); end if;
  return json_build_object('ok', true, 'grant', g);
end $$;

revoke all on function public.app_flags(), public.pay_pending(), public.pay_claim(uuid) from public;
grant execute on function public.app_flags() to anon, authenticated;
grant execute on function public.pay_pending(), public.pay_claim(uuid) to authenticated;
revoke all on function public.grant_purchase(uuid, text, text, text) from public, anon, authenticated;
grant execute on function public.grant_purchase(uuid, text, text, text) to service_role;
