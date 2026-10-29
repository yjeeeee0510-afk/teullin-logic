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
