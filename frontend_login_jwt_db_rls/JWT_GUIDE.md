# DB 로그인과 JWT 동작 흐름

## 실행

터미널 1:

```powershell
cd backend_login_jwt_db_rls
uvicorn app.main:app --reload
```

터미널 2:

```powershell
cd frontend_login_jwt_db_rls
streamlit run app.py
```

고정된 `id01 / pwd01` 계정은 사용하지 않습니다. 회원가입 화면에서 Supabase에 계정을 만든 후 그 계정으로 로그인합니다.

## 동작 흐름

1. 회원가입 화면이 `/auth/signup`을 호출합니다.
2. 백엔드가 비밀번호를 해시하여 Supabase customers에 저장합니다.
3. 로그인 화면이 `/auth/login`을 호출합니다.
4. 백엔드가 DB 비밀번호를 비교하고 JWT를 발급합니다.
5. 프론트엔드가 JWT를 Session Storage에 저장합니다.
6. Product와 Chat 요청에 `Authorization: Bearer <JWT>`를 보냅니다.
7. 로그아웃하면 저장한 JWT를 삭제합니다.

Supabase 설정은 `backend_login_jwt_db_rls/DB_GUIDE.md`를 참고하세요.
