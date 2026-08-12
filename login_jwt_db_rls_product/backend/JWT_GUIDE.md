# Supabase Access Token과 RLS 흐름

이 예제는 자체 JWT를 만들지 않고 Supabase Auth가 발급한 Access Token을 사용합니다.

```text
이메일·비밀번호 로그인
→ Supabase Auth가 Access Token 발급
→ 프론트엔드가 Authorization: Bearer 토큰 전송
→ FastAPI가 토큰과 사용자 역할 확인
→ 사용자 토큰으로 Supabase Product API 호출
→ PostgreSQL RLS가 권한을 최종 확인
```

RLS(Row Level Security)는 데이터베이스가 각 행의 접근 가능 여부를 정책으로 검사하는 기능입니다. Supabase Data API가 Access Token을 검증하면 PostgreSQL의 `auth.uid()`가 로그인 사용자의 UUID를 반환하고, RLS는 이 값과 역할 정보를 이용해 요청을 허용하거나 차단합니다.

일반 사용자의 Product 변경 요청은 FastAPI에서 403으로 차단됩니다. 라우터 검사를 실수로 빠뜨리더라도 RLS 정책이 INSERT, UPDATE, DELETE를 허용하지 않습니다.

`service_role` 키는 RLS를 우회하므로 Product CRUD에 사용하지 않습니다.
