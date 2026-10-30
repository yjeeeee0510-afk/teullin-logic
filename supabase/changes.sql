-- 틀린로직맞추기 랭킹 서버에 실행한 SQL 기록 (Supabase SQL Editor에서 실행)
-- 처음 서버를 만들 때 쓴 표·함수(leaderboard, progress, leaderboard_top/me, delete_my_account,
-- leaderboard_keep_best 트리거)는 그 위에 이 변경들이 차례로 더해진 상태다.

-- 2026-10-28 · 360라운드(난이도 4단계)로 늘리면서 제한 넓힘
alter table public.leaderboard drop constraint if exists leaderboard_best_round_check;
alter table public.leaderboard add constraint leaderboard_best_round_check check (best_round between 0 and 360);
alter table public.leaderboard drop constraint if exists leaderboard_stars_check;
alter table public.leaderboard add constraint leaderboard_stars_check check (stars between 0 and 1080);

-- 2026-10-28 · 프로필 사진(십이지 친구 0~11) 칸과 랭킹 함수
alter table public.leaderboard add column if not exists avatar int;
alter table public.leaderboard drop constraint if exists leaderboard_avatar_check;
alter table public.leaderboard add constraint leaderboard_avatar_check check (avatar is null or avatar between 0 and 11);

drop function if exists public.leaderboard_top(int);
drop function if exists public.leaderboard_me();

create function public.leaderboard_top(n int default 50)
returns table (rank bigint, nickname text, best_round int, stars int, score int, clears int, avg_time int, avatar int, is_me boolean)
language sql stable security definer set search_path = public as $$
  select r.rank, r.nickname, r.best_round, r.stars, r.score, r.clears, r.avg_time, r.avatar, coalesce(r.id = auth.uid(), false) as is_me
  from (select l.*, rank() over (order by l.best_round desc, l.stars desc, l.score desc) as rank from public.leaderboard l) r
  order by r.rank, r.updated_at
  limit greatest(1, least(coalesce(n, 50), 200));
$$;

create function public.leaderboard_me()
returns table (rank bigint, total bigint, nickname text, best_round int, stars int, score int, clears int, avg_time int, avatar int)
language sql stable security definer set search_path = public as $$
  select r.rank, (select count(*) from public.leaderboard), r.nickname, r.best_round, r.stars, r.score, r.clears, r.avg_time, r.avatar
  from (select l.*, rank() over (order by l.best_round desc, l.stars desc, l.score desc) as rank from public.leaderboard l) r
  where r.id = auth.uid();
$$;

grant execute on function public.leaderboard_top(int) to anon, authenticated;
grant execute on function public.leaderboard_me()     to authenticated;

-- 2026-10-28 · 운영진 아이디(yjeeeee0510) 랭킹에서 지우고 앞으로도 막기
delete from public.leaderboard
where id in (select id from auth.users where email = 'yjeeeee0510@teullin.game');

create or replace function public.leaderboard_skip_admin()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  if exists (select 1 from auth.users where id = new.id and email = 'yjeeeee0510@teullin.game') then
    return null;
  end if;
  return new;
end $$;

drop trigger if exists leaderboard_skip_admin on public.leaderboard;
create trigger leaderboard_skip_admin
  before insert or update on public.leaderboard
  for each row execute function public.leaderboard_skip_admin();

-- 2026-10-29 · 하늘섬(361~510라운드) 추가로 제한 넓힘 (라운드 510, 별 510×3)
alter table public.leaderboard drop constraint if exists leaderboard_best_round_check;
alter table public.leaderboard add constraint leaderboard_best_round_check check (best_round between 0 and 510);
alter table public.leaderboard drop constraint if exists leaderboard_stars_check;
alter table public.leaderboard add constraint leaderboard_stars_check check (stars between 0 and 1530);

-- 2026-10-29 · 지도에 다른 플레이어 표시용: 아이디로 로그인한 계정(게스트 제외)만 돌려주는 함수
create or replace function public.leaderboard_players(n int default 300)
returns table (rank bigint, nickname text, best_round int, stars int, avatar int, is_me boolean)
language sql stable security definer set search_path = public as $$
  select r.rank, r.nickname, r.best_round, r.stars, r.avatar, coalesce(r.id = auth.uid(), false) as is_me
  from (select l.*, rank() over (order by l.best_round desc, l.stars desc, l.score desc) as rank from public.leaderboard l) r
  join auth.users u on u.id = r.id
  where coalesce(u.is_anonymous, false) = false and u.email like '%@teullin.game'
  order by r.rank, r.updated_at
  limit greatest(1, least(coalesce(n, 300), 500));
$$;

grant execute on function public.leaderboard_players(int) to anon, authenticated;

-- 2026-10-29 · 칭호 칸 추가, 랭킹·지도 함수가 칭호도 돌려주게
alter table public.leaderboard add column if not exists title text;
alter table public.leaderboard drop constraint if exists leaderboard_title_check;
alter table public.leaderboard add constraint leaderboard_title_check check (title is null or char_length(title) <= 20);

drop function if exists public.leaderboard_top(int);
create function public.leaderboard_top(n int default 50)
returns table (rank bigint, nickname text, best_round int, stars int, score int, clears int, avg_time int, avatar int, is_me boolean, title text)
language sql stable security definer set search_path = public as $$
  select r.rank, r.nickname, r.best_round, r.stars, r.score, r.clears, r.avg_time, r.avatar, coalesce(r.id = auth.uid(), false) as is_me, r.title
  from (select l.*, rank() over (order by l.best_round desc, l.stars desc, l.score desc) as rank from public.leaderboard l) r
  order by r.rank, r.updated_at
  limit greatest(1, least(coalesce(n, 50), 200));
$$;

drop function if exists public.leaderboard_players(int);
create function public.leaderboard_players(n int default 300)
returns table (rank bigint, nickname text, best_round int, stars int, avatar int, is_me boolean, title text)
language sql stable security definer set search_path = public as $$
  select r.rank, r.nickname, r.best_round, r.stars, r.avatar, coalesce(r.id = auth.uid(), false) as is_me, r.title
  from (select l.*, rank() over (order by l.best_round desc, l.stars desc, l.score desc) as rank from public.leaderboard l) r
  join auth.users u on u.id = r.id
  where coalesce(u.is_anonymous, false) = false and u.email like '%@teullin.game'
  order by r.rank, r.updated_at
  limit greatest(1, least(coalesce(n, 300), 500));
$$;

grant execute on function public.leaderboard_top(int) to anon, authenticated;
grant execute on function public.leaderboard_players(int) to anon, authenticated;

-- 2026-10-29 · dhsb1234도 운영진: 랭킹에서 지우고 앞으로도 막기
delete from public.leaderboard
where id in (select id from auth.users where email in ('yjeeeee0510@teullin.game','dhsb1234@teullin.game'));

create or replace function public.leaderboard_skip_admin()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  if exists (select 1 from auth.users where id = new.id and email in ('yjeeeee0510@teullin.game','dhsb1234@teullin.game')) then
    return null;
  end if;
  return new;
end $$;

-- 2026-10-29 · 운영진 접속 중인 사람 보기
-- 접속 중인 사람 보기 (운영진 전용)
create table if not exists public.presence (
  id uuid primary key references auth.users(id) on delete cascade,
  nickname text,
  avatar int,
  online boolean not null default true,
  since timestamptz not null default now(),
  last_seen timestamptz not null default now()
);
alter table public.presence enable row level security;
drop policy if exists presence_insert_own on public.presence;
create policy presence_insert_own on public.presence for insert to authenticated with check (auth.uid() = id);
drop policy if exists presence_update_own on public.presence;
create policy presence_update_own on public.presence for update to authenticated using (auth.uid() = id) with check (auth.uid() = id);
drop policy if exists presence_select_own on public.presence;
create policy presence_select_own on public.presence for select to authenticated using (auth.uid() = id);

-- 시간은 서버가 정한다. 2분 넘게 끊겼다가 다시 오면 접속 시작 시간을 새로
create or replace function public.presence_touch() returns trigger language plpgsql as $$
begin
  if tg_op = 'INSERT' or old.last_seen < now() - interval '2 minutes' or not old.online then new.since := now();
  else new.since := old.since; end if;
  new.last_seen := now();
  new.nickname := left(coalesce(new.nickname, ''), 30);
  return new;
end $$;
drop trigger if exists presence_touch on public.presence;
create trigger presence_touch before insert or update on public.presence for each row execute function public.presence_touch();

-- 운영진만: 최근 90초 안에 신호가 온 사람
create or replace function public.presence_online()
returns table (nickname text, avatar int, account text, is_guest boolean, since timestamptz, last_seen timestamptz)
language sql security definer set search_path = public as $$
  select p.nickname, p.avatar,
         case when u.is_anonymous then null else split_part(u.email, '@', 1) end,
         coalesce(u.is_anonymous, true), p.since, p.last_seen
  from public.presence p join auth.users u on u.id = p.id
  where p.online and p.last_seen > now() - interval '90 seconds'
    and (auth.jwt() ->> 'email') in ('yjeeeee0510@teullin.game', 'dhsb1234@teullin.game')
  order by coalesce(u.is_anonymous, true), p.since;
$$;
revoke all on function public.presence_online() from public, anon;
grant execute on function public.presence_online() to authenticated;

-- 2026-10-30 · 과자 나라 순위 (tools/candy/ranking.sql 그대로)
-- 과자 나라 순위: leaderboard 표에 칸 3개 + 순위 함수 2개 (사용자가 SQL Editor에서 실행)
alter table public.leaderboard add column if not exists candy_round int not null default 0;
alter table public.leaderboard add column if not exists candy_stars int not null default 0;
alter table public.leaderboard add column if not exists candy_time int not null default 0;
alter table public.leaderboard drop constraint if exists leaderboard_candy_check;
alter table public.leaderboard add constraint leaderboard_candy_check
  check (candy_round between 0 and 300 and candy_stars between 0 and 900 and candy_time between 0 and 86400);

create or replace function public.leaderboard_candy_top(n int default 50)
returns table (rank bigint, nickname text, candy_round int, candy_stars int, candy_time int, avatar int, is_me boolean, title text)
language sql stable security definer set search_path = public as $$
  select r.rank, r.nickname, r.candy_round, r.candy_stars, r.candy_time, r.avatar, coalesce(r.id = auth.uid(), false) as is_me, r.title
  from (select l.*, rank() over (order by l.candy_round desc, l.candy_stars desc, nullif(l.candy_time, 0) asc nulls last) as rank
        from public.leaderboard l where l.candy_round > 0) r
  order by r.rank, r.updated_at
  limit greatest(1, least(coalesce(n, 50), 200));
$$;

create or replace function public.leaderboard_candy_me()
returns table (rank bigint, total bigint, nickname text, candy_round int, candy_stars int, candy_time int)
language sql stable security definer set search_path = public as $$
  select r.rank, r.total, r.nickname, r.candy_round, r.candy_stars, r.candy_time
  from (select l.*, rank() over (order by l.candy_round desc, l.candy_stars desc, nullif(l.candy_time, 0) asc nulls last) as rank,
               count(*) over () as total
        from public.leaderboard l where l.candy_round > 0) r
  where r.id = auth.uid();
$$;

grant execute on function public.leaderboard_candy_top(int) to anon, authenticated;
grant execute on function public.leaderboard_candy_me() to authenticated;

-- 2026-10-30 · 지도에 모든 플레이어 표시: 아이디 계정 + 게스트 (랭킹에 기록이 있는 사람 모두)
create or replace function public.leaderboard_players(n int default 300)
returns table (rank bigint, nickname text, best_round int, stars int, avatar int, is_me boolean, title text)
language sql stable security definer set search_path = public as $$
  select r.rank, r.nickname, r.best_round, r.stars, r.avatar, coalesce(r.id = auth.uid(), false) as is_me, r.title
  from (select l.*, rank() over (order by l.best_round desc, l.stars desc, l.score desc) as rank from public.leaderboard l) r
  where coalesce(r.nickname, '') <> ''
  order by r.rank, r.updated_at
  limit greatest(1, least(coalesce(n, 300), 500));
$$;
grant execute on function public.leaderboard_players(int) to anon, authenticated;

-- ============================================================
-- 2026-10-30 test1 계정에 섞인 운영진(yjeeeee0510) 기록 정리 (실행 완료)
-- 원인: 한 기기에서 아이디를 바꿔 로그인할 때 기기 기록이 합쳐짐 → 패치 3.9에서 고침
-- 1) 운영진 기록과 똑같은 라운드(151·212·355·360·361)만 지우고 열린 라운드 91·열린 지역 1(푸른 바다)
with t as (select id from auth.users where email='test1@teullin.game'),
a as (select p.data->'rounds' r from public.progress p join auth.users u on u.id=p.id where u.email='yjeeeee0510@teullin.game')
update public.progress p
set data = jsonb_set(jsonb_set(jsonb_set(p.data,'{rounds}',
      coalesce((select jsonb_object_agg(k,v) from jsonb_each(p.data->'rounds') e(k,v)
                where not (k in ('151','212','355','360','361') and v = (select r->k from a))),'{}'::jsonb)),
    '{unlocked}','91'::jsonb),'{revealed}','1'::jsonb),
    updated_at = now()
where p.id = (select id from t);
-- 2) 랭킹 다시 계산 (leaderboard_keep_best 트리거가 낮추는 걸 막으므로 이번 한 번만 끄고 다시 켬)
begin;
alter table public.leaderboard disable trigger leaderboard_keep_best;
with t as (select id from auth.users where email='test1@teullin.game'),
r as (select (k)::int rk, v from public.progress p, jsonb_each(p.data->'rounds') e(k,v) where p.id=(select id from t))
update public.leaderboard l set
  best_round = coalesce((select max(rk) from r),0),
  stars = coalesce((select sum(coalesce((v->>'stars')::int,1)) from r),0),
  score = coalesce((select sum(coalesce((v->>'best')::int,0)) from r),0),
  clears = coalesce((select sum(coalesce((v->>'plays')::int,1)) from r),0),
  avg_time = coalesce((select round(avg((v->>'time')::numeric)) from r where (v->>'time')::numeric>0),0)
where l.id = (select id from t);
alter table public.leaderboard enable trigger leaderboard_keep_best;
commit;
-- 결과: test1 최고 90라운드·별 270·점수 65861·라운드 90개, 열린 라운드 91·지역 1

-- ============================================================
-- 2026-10-30 랭킹 정리 (실행 완료)
begin;
-- 1) 게스트 '중독군'·'호랑이' 랭킹 기록 삭제 (4줄)
delete from public.leaderboard where id in (
  '1fe9d08f-c6da-492d-84f4-ccbb2f725349','8a262c16-91b9-45c3-8cde-8a52c0057e73',
  '863a0002-3ab5-4588-bc29-b34980d7b7f3','dca67f98-2484-4305-bd72-723bbbda6a8b');
-- 2) test1 과자 나라·칭호에 섞인 운영진 기록 정리 (운영진과 같은 과자 라운드 20개·오늘의 과자·도장·과자 업적·칭호·테두리)
with t as (select id from auth.users where email='test1@teullin.game'),
a as (select p.data->'candy'->'rounds' r from public.progress p join auth.users u on u.id=p.id where u.email='yjeeeee0510@teullin.game')
update public.progress p set data =
  ((((p.data #- '{ach,got,candyStar}') #- '{ach,got,candyClear}') #- '{ach,got,candyDaily}') - 'frame')
  || jsonb_build_object('candy', (p.data->'candy') || jsonb_build_object(
       'rounds', coalesce((select jsonb_object_agg(k,v) from jsonb_each(p.data->'candy'->'rounds') e(k,v) where v is distinct from (select r->k from a)),'{}'::jsonb),
       'unlocked',4,'daily','{}'::jsonb,'months','{}'::jsonb),
     'title',null,'titleAt',(extract(epoch from now())*1000)::bigint,'frameAt',(extract(epoch from now())*1000)::bigint),
  updated_at = now()
where p.id=(select id from t);
-- 3) test1 랭킹의 과자 나라 기록·칭호 다시 계산
with t as (select id from auth.users where email='test1@teullin.game'),
r as (select k::int rk, v from public.progress p, jsonb_each(p.data->'candy'->'rounds') e(k,v) where p.id=(select id from t))
update public.leaderboard l set
  candy_round = coalesce((select max(rk) from r),0),
  candy_stars = coalesce((select sum(coalesce((v->>'stars')::int,1)) from r),0),
  candy_time  = coalesce((select round(avg((v->>'time')::numeric)) from r where (v->>'time')::numeric>0),0),
  title = null
where l.id=(select id from t);
commit;
-- 결과: 랭킹 9명, test1 과자 나라 3라운드·별 9, 칭호 없음
