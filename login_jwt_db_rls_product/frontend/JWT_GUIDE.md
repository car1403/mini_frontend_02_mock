# 프론트엔드 Access Token 처리

로그인 응답의 `access_token`과 `user.role`을 Session Storage에 저장합니다. API 요청에는 다음 헤더가 자동으로 추가됩니다.

```text
Authorization: Bearer 사용자의-Supabase-Access-Token
```

역할에 따른 메뉴 분리는 사용자 편의를 위한 것이며, 실제 권한은 FastAPI와 Supabase RLS가 검사합니다.
