-- 2026-11-14 · 패치 6.8 구글 로그인 — 운영진 판별에 구글 이메일 추가 (대표가 SQL Editor에서 직접 실행)
-- 운영진 = yjeeeee0510@gmail.com (D-004). 기존 아이디 운영진(yjeeeee0510·dhsb1234 @teullin.game)은 과도기 동안 유지(O-005).
-- 실행하지 않아도 게임은 동작하지만, 운영진 계정이 랭킹에 올라가고 운영진 전용 함수가 거절된다.

-- 1) 운영진은 랭킹에서 제외: 이미 올라간 기록 지우고 앞으로도 막기
delete from public.leaderboard
where id in (select id from auth.users where email in ('yjeeeee0510@teullin.game','dhsb1234@teullin.game','yjeeeee0510@gmail.com'));

create or replace function public.leaderboard_skip_admin()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  if exists (select 1 from auth.users where id = new.id and email in ('yjeeeee0510@teullin.game','dhsb1234@teullin.game','yjeeeee0510@gmail.com')) then
    return null;
  end if;
  return new;
end $$;

-- 2) 접속 중인 사람 보기(운영진 전용): 구글 계정은 account에 전체 이메일을 돌려줘서, 아이디(yjeeeee0510)와 겹쳐 운영진으로 잘못 표시되지 않게 함
create or replace function public.presence_online()
returns table (nickname text, avatar int, account text, is_guest boolean, since timestamptz, last_seen timestamptz)
language sql security definer set search_path = public as $$
  select p.nickname, p.avatar,
         case when u.is_anonymous then null
              when u.email like '%@teullin.game' then split_part(u.email, '@', 1)
              else lower(u.email) end,
         coalesce(u.is_anonymous, true), p.since, p.last_seen
  from public.presence p join auth.users u on u.id = p.id
  where p.online and p.last_seen > now() - interval '90 seconds'
    and (auth.jwt() ->> 'email') in ('yjeeeee0510@teullin.game', 'dhsb1234@teullin.game', 'yjeeeee0510@gmail.com')
  order by coalesce(u.is_anonymous, true), p.since;
$$;
revoke all on function public.presence_online() from public, anon;
grant execute on function public.presence_online() to authenticated;

-- 3) 운영진이 기존 아이디 계정의 비밀번호를 바꾸는 함수: 운영진 판별에 구글 이메일 추가 (대상은 여전히 @teullin.game 아이디만)
create extension if not exists pgcrypto with schema extensions;
create or replace function public.admin_set_password(target_id text, new_password text)
returns json
language plpgsql security definer set search_path = public, extensions as $$
declare
  target_email text;
  uid uuid;
begin
  if coalesce(auth.jwt() ->> 'email', '') not in ('yjeeeee0510@teullin.game','dhsb1234@teullin.game','yjeeeee0510@gmail.com') then
    raise exception 'not_admin' using errcode = '42501';
  end if;
  if new_password is null or length(new_password) < 6 then
    raise exception 'weak_password' using errcode = 'P0001';
  end if;
  target_email := lower(trim(target_id)) || '@teullin.game';
  select id into uid from auth.users where email = target_email;
  if uid is null then
    return json_build_object('ok', false, 'reason', 'no_user');
  end if;
  update auth.users
     set encrypted_password = extensions.crypt(new_password, extensions.gen_salt('bf')),
         updated_at = now()
   where id = uid;
  return json_build_object('ok', true, 'id', lower(trim(target_id)));
end $$;
revoke all on function public.admin_set_password(text, text) from public, anon;
grant execute on function public.admin_set_password(text, text) to authenticated;
