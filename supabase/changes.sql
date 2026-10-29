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
