-- Supabase Dashboard > SQL Editor에서 실행합니다.

CREATE TABLE IF NOT EXISTS public.customers (
    id TEXT PRIMARY KEY,
    pwd TEXT NOT NULL,
    name TEXT NOT NULL
);

COMMENT ON TABLE public.customers
IS 'JWT 예제의 회원 정보를 저장하는 테이블';

COMMENT ON COLUMN public.customers.pwd
IS '평문 비밀번호가 아닌 PBKDF2 해시 문자열';

-- frontend가 Supabase를 직접 호출하지 못하도록 RLS를 활성화합니다.
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;

