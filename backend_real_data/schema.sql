-- Supabase Dashboard의 SQL Editor에서 실행하세요.

create table if not exists public.realtime_sensor_data (
    id uuid primary key default gen_random_uuid(),
    device_name text not null,
    temperature double precision not null,
    humidity double precision not null
        check (humidity >= 0 and humidity <= 100),
    created_by text not null,
    created_at timestamptz not null default now()
);

create index if not exists realtime_sensor_data_created_at_idx
on public.realtime_sensor_data (created_at desc);

comment on table public.realtime_sensor_data
is 'JWT 로그인 사용자가 입력한 실시간 센서 데이터';

-- 이 예제는 백엔드에서 service_role key로만 접근합니다.
-- 프론트엔드가 Supabase에 직접 접근하지 못하도록 RLS를 활성화합니다.
alter table public.realtime_sensor_data enable row level security;

-- service_role은 RLS를 우회할 수 있으므로 별도 policy가 필요하지 않습니다.
-- service_role key는 frontend나 Git 저장소에 절대 공개하면 안 됩니다.
