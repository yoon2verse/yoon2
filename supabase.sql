-- Supabase → SQL Editor 에 붙여넣고 Run
create table if not exists guests (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 1 and 8),
  msg  text not null check (char_length(msg) between 1 and 60),
  look jsonb not null,
  ts   bigint not null,
  created_at timestamptz default now()
);
alter table guests enable row level security;
create policy "anyone can read"  on guests for select using (true);
create policy "anyone can write" on guests for insert with check (true);
