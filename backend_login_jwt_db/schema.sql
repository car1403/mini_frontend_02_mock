-- Supabase Dashboard > SQL Editor에서 실행합니다.

CREATE TABLE IF NOT EXISTS public.customers (
    id TEXT PRIMARY KEY,
    pwd TEXT NOT NULL,
    name TEXT NOT NULL
);
