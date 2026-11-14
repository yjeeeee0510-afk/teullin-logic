-- 2026-11-14 · 패치 6.9 우편함·운영진 발송 (대표가 SQL Editor에서 직접 실행)
-- 실행하기 전에도 게임은 정상 동작한다(우편함 아이콘만 안 보임).
-- 결정: D-007(우편함) D-008(운영진 발송) D-011(전체 우편은 보관 기간 안 신규 가입자도 받음, 게스트는 못 받음, 보관 30일)
-- 보상 상한(실수 방지): 코인 10,000 · 힌트/하트/쿠키 하트 각 20

create table if not exists public.mail (
  id uuid primary key default gen_random_uuid(),
  kind text not null default 'staff' check (kind in ('staff','system')),
  title text not null check (char_length(title) between 1 and 40),
  body text not null default '' check (char_length(body) <= 500),
  coins int not null default 0 check (coins between 0 and 10000),
  hints int not null default 0 check (hints between 0 and 20),
  hearts int not null default 0 check (hearts between 0 and 20),
  cookies int not null default 0 check (cookies between 0 and 20),
  target text not null check (target in ('all','user')),   -- all: 보관 기간 안에 로그인하는 모두 · user: mail_box에 적힌 사람만
  note text not null default '',                           -- 발송 기록용 대상 설명
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '30 days',
  created_by uuid
);
create table if not exists public.mail_box (
  mail_id uuid not null references public.mail(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  read_at timestamptz,
  claimed_at timestamptz,
  deleted_at timestamptz,
  primary key (mail_id, user_id)
);
create index if not exists mail_box_user_idx on public.mail_box(user_id);
create index if not exists mail_created_idx on public.mail(created_at desc);

-- 표는 서버 함수로만 읽고 쓴다(직접 접근 막음)
alter table public.mail enable row level security;
alter table public.mail_box enable row level security;
revoke all on public.mail, public.mail_box from anon, authenticated;

-- 내 우편함 (게스트는 빈 목록)
create or replace function public.mail_inbox()
returns table (id uuid, kind text, title text, body text, coins int, hints int, hearts int, cookies int,
               created_at timestamptz, expires_at timestamptz, read_at timestamptz, claimed_at timestamptz)
language sql stable security definer set search_path = public as $$
  select m.id, m.kind, m.title, m.body, m.coins, m.hints, m.hearts, m.cookies, m.created_at, m.expires_at, b.read_at, b.claimed_at
  from public.mail m
  left join public.mail_box b on b.mail_id = m.id and b.user_id = auth.uid()
  where auth.uid() is not null
    and coalesce((auth.jwt() ->> 'is_anonymous')::boolean, false) = false
    and m.expires_at > now()
    and b.deleted_at is null
    and (m.target = 'all' or b.user_id is not null)
  order by m.created_at desc
  limit 50;
$$;

create or replace function public.mail_read(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null or coalesce((auth.jwt() ->> 'is_anonymous')::boolean, false) then return; end if;
  if not exists (select 1 from public.mail m where m.id = p_id and m.expires_at > now()
                   and (m.target = 'all' or exists (select 1 from public.mail_box b where b.mail_id = m.id and b.user_id = auth.uid()))) then return; end if;
  insert into public.mail_box (mail_id, user_id, read_at) values (p_id, auth.uid(), now())
  on conflict (mail_id, user_id) do update set read_at = coalesce(public.mail_box.read_at, now());
end $$;

create or replace function public.mail_delete(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null or coalesce((auth.jwt() ->> 'is_anonymous')::boolean, false) then return; end if;
  if not exists (select 1 from public.mail m where m.id = p_id
                   and (m.target = 'all' or exists (select 1 from public.mail_box b where b.mail_id = m.id and b.user_id = auth.uid()))) then return; end if;
  insert into public.mail_box (mail_id, user_id, read_at, deleted_at) values (p_id, auth.uid(), now(), now())
  on conflict (mail_id, user_id) do update set deleted_at = now(), read_at = coalesce(public.mail_box.read_at, now());
end $$;

-- 받기: 같은 우편은 서버 기록으로 딱 한 번만 보상이 나간다
create or replace function public.mail_claim(p_id uuid)
returns json language plpgsql security definer set search_path = public as $$
declare m public.mail; n int;
begin
  if auth.uid() is null or coalesce((auth.jwt() ->> 'is_anonymous')::boolean, false) then
    return json_build_object('ok', false, 'reason', 'guest');
  end if;
  select * into m from public.mail where id = p_id and expires_at > now();
  if not found then return json_build_object('ok', false, 'reason', 'gone'); end if;
  if m.target = 'user' and not exists (select 1 from public.mail_box b where b.mail_id = p_id and b.user_id = auth.uid()) then
    return json_build_object('ok', false, 'reason', 'gone');
  end if;
  insert into public.mail_box (mail_id, user_id, read_at, claimed_at) values (p_id, auth.uid(), now(), now())
  on conflict (mail_id, user_id) do update set claimed_at = now(), read_at = coalesce(public.mail_box.read_at, now())
    where public.mail_box.claimed_at is null and public.mail_box.deleted_at is null;
  get diagnostics n = row_count;
  if n = 0 then return json_build_object('ok', false, 'reason', 'already'); end if;
  return json_build_object('ok', true, 'id', m.id, 'coins', m.coins, 'hints', m.hints, 'hearts', m.hearts, 'cookies', m.cookies);
end $$;

create or replace function public.mail_claim_all()
returns json language plpgsql security definer set search_path = public as $$
declare r record; res json; c int := 0; h int := 0; hr int := 0; ck int := 0; k int := 0;
begin
  for r in select i.id from public.mail_inbox() i where i.claimed_at is null and (i.coins + i.hints + i.hearts + i.cookies) > 0 loop
    res := public.mail_claim(r.id);
    if (res ->> 'ok')::boolean then
      c := c + (res ->> 'coins')::int; h := h + (res ->> 'hints')::int; hr := hr + (res ->> 'hearts')::int; ck := ck + (res ->> 'cookies')::int; k := k + 1;
    end if;
  end loop;
  return json_build_object('ok', true, 'count', k, 'coins', c, 'hints', h, 'hearts', hr, 'cookies', ck);
end $$;

-- ===== 운영진 전용 (구글 이메일 yjeeeee0510@gmail.com 만 통과, D-004·D-008) =====
create or replace function public._mail_is_admin() returns boolean
language sql stable as $$ select coalesce(auth.jwt() ->> 'email', '') = 'yjeeeee0510@gmail.com' $$;

-- 개별 발송 대상 찾기: 닉네임 또는 계정으로 검색 (게스트 제외). 받는 사람은 서버 내부 ID로 구분한다.
create or replace function public.admin_find_users(p_q text)
returns table (id uuid, nickname text, account text, last_seen timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public._mail_is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  return query
    select u.id, coalesce(l.nickname, p.nickname, ''),
           case when u.email like '%@teullin.game' then split_part(u.email, '@', 1) else lower(u.email) end,
           p.last_seen
    from auth.users u
    left join public.leaderboard l on l.id = u.id
    left join public.presence p on p.id = u.id
    where coalesce(u.is_anonymous, false) = false
      and length(trim(coalesce(p_q, ''))) >= 1
      and (coalesce(l.nickname, p.nickname, '') ilike '%' || trim(p_q) || '%' or lower(u.email) like '%' || lower(trim(p_q)) || '%')
    order by p.last_seen desc nulls last
    limit 20;
end $$;

-- 대상 계산 (p_dry = true 이면 인원만 세어 돌려줌 → 화면의 "N명에게 보냅니다" 확인용)
-- p_mode: all(전체) · ids(개별) · online(접속 중) · round(특정 라운드 이상) · recent(최근 N일 접속)
create or replace function public.admin_send_mail(
  p_mode text, p_ids uuid[], p_min_round int, p_days int,
  p_kind text, p_title text, p_body text, p_coins int, p_hints int, p_hearts int, p_cookies int, p_dry boolean default false)
returns json language plpgsql security definer set search_path = public as $$
declare ids uuid[]; cnt int; mid uuid; note text;
begin
  if not public._mail_is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  if p_mode = 'all' then
    select count(*) into cnt from auth.users u where coalesce(u.is_anonymous, false) = false;
    note := '전체(보관 기간 안 로그인하는 모든 계정)';
  elsif p_mode = 'ids' then
    select array_agg(u.id) into ids from auth.users u where u.id = any(coalesce(p_ids, '{}')) and coalesce(u.is_anonymous, false) = false;
    cnt := coalesce(array_length(ids, 1), 0); note := '개별 ' || cnt || '명';
  elsif p_mode = 'online' then
    select array_agg(p.id) into ids from public.presence p join auth.users u on u.id = p.id
     where p.online and p.last_seen > now() - interval '90 seconds' and coalesce(u.is_anonymous, false) = false;
    cnt := coalesce(array_length(ids, 1), 0); note := '접속 중 ' || cnt || '명';
  elsif p_mode = 'round' then
    select array_agg(l.id) into ids from public.leaderboard l join auth.users u on u.id = l.id
     where l.best_round >= greatest(coalesce(p_min_round, 1), 1) and coalesce(u.is_anonymous, false) = false;
    cnt := coalesce(array_length(ids, 1), 0); note := greatest(coalesce(p_min_round, 1), 1) || '라운드 이상 ' || cnt || '명';
  elsif p_mode = 'recent' then
    select array_agg(p.id) into ids from public.presence p join auth.users u on u.id = p.id
     where p.last_seen > now() - make_interval(days => greatest(coalesce(p_days, 1), 1)) and coalesce(u.is_anonymous, false) = false;
    cnt := coalesce(array_length(ids, 1), 0); note := '최근 ' || greatest(coalesce(p_days, 1), 1) || '일 접속 ' || cnt || '명';
  else
    return json_build_object('ok', false, 'reason', 'mode');
  end if;
  if p_dry then return json_build_object('ok', true, 'count', cnt, 'note', note); end if;
  if cnt = 0 then return json_build_object('ok', false, 'reason', 'nobody'); end if;
  if p_kind not in ('staff', 'system') then return json_build_object('ok', false, 'reason', 'kind'); end if;
  insert into public.mail (kind, title, body, coins, hints, hearts, cookies, target, note, created_by)
  values (p_kind, left(trim(coalesce(p_title, '')), 40), left(coalesce(p_body, ''), 500),
          coalesce(p_coins, 0), coalesce(p_hints, 0), coalesce(p_hearts, 0), coalesce(p_cookies, 0),
          case when p_mode = 'all' then 'all' else 'user' end, note, auth.uid())
  returning id into mid;
  if p_mode <> 'all' then
    insert into public.mail_box (mail_id, user_id) select mid, x from unnest(ids) x;
  end if;
  return json_build_object('ok', true, 'count', cnt, 'id', mid, 'note', note);
end $$;

-- 보낸 기록 (최근 50통)
create or replace function public.admin_mail_log()
returns table (id uuid, kind text, title text, coins int, hints int, hearts int, cookies int, note text, created_at timestamptz, expires_at timestamptz, claimed bigint)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public._mail_is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  return query
    select m.id, m.kind, m.title, m.coins, m.hints, m.hearts, m.cookies, m.note, m.created_at, m.expires_at,
           (select count(*) from public.mail_box b where b.mail_id = m.id and b.claimed_at is not null)
    from public.mail m order by m.created_at desc limit 50;
end $$;

revoke all on function public.mail_inbox(), public.mail_read(uuid), public.mail_delete(uuid), public.mail_claim(uuid), public.mail_claim_all() from public, anon;
grant execute on function public.mail_inbox(), public.mail_read(uuid), public.mail_delete(uuid), public.mail_claim(uuid), public.mail_claim_all() to authenticated;
revoke all on function public._mail_is_admin() from public, anon;
revoke all on function public.admin_find_users(text), public.admin_mail_log() from public, anon;
revoke all on function public.admin_send_mail(text, uuid[], int, int, text, text, text, int, int, int, int, boolean) from public, anon;
grant execute on function public.admin_find_users(text), public.admin_mail_log() to authenticated;
grant execute on function public.admin_send_mail(text, uuid[], int, int, text, text, text, int, int, int, int, boolean) to authenticated;
grant execute on function public._mail_is_admin() to authenticated;
