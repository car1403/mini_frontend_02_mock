-- Supabase Dashboard의 SQL Editor에서 실행하세요.

create table if not exists public.realtime_sensor_data (
    id uuid primary key default gen_random_uuid(),
    device_name text not null,
    temperature double precision not null,
    humidity double precision not null
        check (humidity >= 0 and humidity <= 100),
    created_at timestamptz not null default now()
);

create index if not exists realtime_sensor_data_created_at_idx
on public.realtime_sensor_data (created_at desc);
