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
