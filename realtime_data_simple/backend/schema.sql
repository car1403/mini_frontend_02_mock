-- Supabase Dashboard의 SQL Editor에서 실행하세요.

create table if not exists public.realtime_sensor_data (
    id uuid primary key default gen_random_uuid(),
    device_name text not null,
    temperature double precision not null,
    humidity double precision not null,
    created_at timestamp not null default now()
);
