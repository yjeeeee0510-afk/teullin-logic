-- 패치 7.7: 기존 아이디 계정 → 구글 계정 기록 이전 (D-019, 승인 A-015·A-016)
-- 실행: Supabase SQL Editor (대표님이 Run). 여러 번 실행해도 안전(if not exists / create or replace).
-- 하는 일
--   1) 구글로 로그인한 사람이 기존 아이디·비밀번호를 대면, 서버가 비밀번호를 확인한 뒤
--      · 랭킹 기록(leaderboard)을 구글 계정으로 옮기고(구글 쪽에 이미 있으면 더 좋은 값 유지),
--      · 진행 기록(progress)은 그대로 돌려줘 앱이 기존 합치기 규칙(mergeP)으로 합치게 하고,
--      · 기존 아이디 계정은 로그인을 막는다(원본 데이터는 지우지 않음 → 되돌릴 수 있음).
--   2) 비밀번호를 틀리면 15분에 5번까지만 시도할 수 있다.
-- 비밀번호·이전 기록은 이 표들에 평문으로 저장하지 않는다.

create table if not exists public.legacy_claims (
  legacy_id  uuid primary key references auth.users(id) on delete cascade,
  google_id  uuid not null references auth.users(id) on delete cascade,
  login      text not null,
  lb_backup  jsonb,                       -- 옮기기 전 기존 아이디의 랭킹 행(되돌리기용)
  claimed_at timestamptz not null default now()
);
alter table public.legacy_claims enable row level security;   -- 정책 없음 = 앱에서 직접 읽기·쓰기 불가

create table if not exists public.legacy_claim_tries (
  uid uuid not null,
  at  timestamptz not null default now()
);
create index if not exists legacy_claim_tries_idx on public.legacy_claim_tries (uid, at);
alter table public.legacy_claim_tries enable row level security;

create or replace function public.claim_legacy_account(p_login text, p_password text)
returns jsonb
language plpgsql
security definer
set search_path = public, extensions, pg_temp
as $$
declare
  me      uuid := auth.uid();
  me_row  auth.users%rowtype;
  leg     auth.users%rowtype;
  lp      public.progress%rowtype;
  ll      public.leaderboard%rowtype;
  fails   int;
  lg      text := lower(btrim(coalesce(p_login, '')));
begin
  if me is null then
    return jsonb_build_object('ok', false, 'error', 'not_signed_in');
  end if;
  select * into me_row from auth.users where id = me;
  -- 구글 등 정식 계정만 받는다(기존 아이디·게스트 불가)
  if me_row.id is null or coalesce(me_row.is_anonymous, false) or me_row.email is null or me_row.email like '%@teullin.game' then
    return jsonb_build_object('ok', false, 'error', 'google_required');
  end if;

  delete from public.legacy_claim_tries where at < now() - interval '1 day';
  select count(*) into fails from public.legacy_claim_tries where uid = me and at > now() - interval '15 minutes';
  if fails >= 5 then
    return jsonb_build_object('ok', false, 'error', 'too_many_tries');
  end if;

  if lg = '' or length(lg) > 40 or length(coalesce(p_password, '')) = 0 or length(p_password) > 200 then
    insert into public.legacy_claim_tries(uid) values (me);
    return jsonb_build_object('ok', false, 'error', 'bad_login');
  end if;

  select * into leg from auth.users where email = lg || '@teullin.game';
  -- 없는 아이디와 틀린 비밀번호는 같은 오류로 돌려준다(아이디 존재 여부를 알려 주지 않음)
  if leg.id is null or leg.encrypted_password is null or leg.encrypted_password = ''
     or extensions.crypt(p_password, leg.encrypted_password) <> leg.encrypted_password then
    insert into public.legacy_claim_tries(uid) values (me);
    return jsonb_build_object('ok', false, 'error', 'bad_login');
  end if;

  if exists (select 1 from public.legacy_claims where legacy_id = leg.id) then
    return jsonb_build_object('ok', false, 'error', 'already_claimed');
  end if;

  select * into lp from public.progress    where id = leg.id;
  select * into ll from public.leaderboard where id = leg.id;

  -- 랭킹 기록 이전: 구글 쪽에 이미 있으면 더 좋은 값만 남김(닉네임·꾸미기는 구글 쪽 우선)
  if ll.id is not null then
    insert into public.leaderboard (id, nickname, best_round, stars, score, clears, avg_time, avatar, title,
                                    candy_round, candy_stars, candy_time, deco)
    values (me, ll.nickname, coalesce(ll.best_round,0), coalesce(ll.stars,0), coalesce(ll.score,0), coalesce(ll.clears,0),
            coalesce(ll.avg_time,0), ll.avatar, ll.title,
            coalesce(ll.candy_round,0), coalesce(ll.candy_stars,0), coalesce(ll.candy_time,0), ll.deco)
    on conflict (id) do update set
      best_round  = greatest(public.leaderboard.best_round,  excluded.best_round),
      stars       = greatest(public.leaderboard.stars,       excluded.stars),
      score       = greatest(public.leaderboard.score,       excluded.score),
      clears      = greatest(public.leaderboard.clears,      excluded.clears),
      candy_round = greatest(public.leaderboard.candy_round, excluded.candy_round),
      candy_stars = greatest(public.leaderboard.candy_stars, excluded.candy_stars),
      avg_time    = case when coalesce(public.leaderboard.avg_time,0)   > 0 then public.leaderboard.avg_time   else excluded.avg_time   end,
      candy_time  = case when coalesce(public.leaderboard.candy_time,0) > 0 then public.leaderboard.candy_time else excluded.candy_time end,
      title       = coalesce(public.leaderboard.title,  excluded.title),
      avatar      = coalesce(public.leaderboard.avatar, excluded.avatar),
      deco        = coalesce(public.leaderboard.deco,   excluded.deco);
  end if;

  insert into public.legacy_claims (legacy_id, google_id, login, lb_backup)
  values (leg.id, me, lg, case when ll.id is not null then to_jsonb(ll) else null end);

  -- 구글 쪽에 랭킹 행이 생겼을 때만 기존 아이디의 중복 랭킹 행을 지운다(운영진 계정처럼 막힌 경우는 그대로 둠)
  if ll.id is not null and exists (select 1 from public.leaderboard where id = me) then
    delete from public.leaderboard where id = leg.id;
  end if;

  -- 기존 아이디 로그인 막기(원본 기록은 남김). 되돌리기: update auth.users set banned_until = null where id = '<legacy id>';
  update auth.users set banned_until = timestamptz '2999-01-01 00:00:00+00' where id = leg.id;
  begin
    delete from auth.sessions where user_id = leg.id;
  exception when others then
    null;   -- 세션 표 구조가 달라도 이전 자체는 성공시킨다(차단은 banned_until로 이미 적용됨)
  end;

  return jsonb_build_object(
    'ok', true,
    'login', lg,
    'progress', coalesce(lp.data, '{}'::jsonb),
    'nickname', ll.nickname
  );
end;
$$;

revoke all on function public.claim_legacy_account(text, text) from public, anon;
grant execute on function public.claim_legacy_account(text, text) to authenticated;
