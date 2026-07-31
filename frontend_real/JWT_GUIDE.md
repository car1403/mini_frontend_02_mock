# JWT 프론트엔드 실행 가이드

## 실행 순서

터미널 1에서 JWT 백엔드를 실행합니다.

```powershell
cd backend_login_jwt
uvicorn app.main:app --reload
```

터미널 2에서 프론트엔드를 실행합니다.

```powershell
cd frontend_login_jwt
streamlit run app.py
```

로그인 정보는 `id01 / pwd01`입니다.

## 동작 흐름

1. 로그인 화면이 `/auth/login`을 호출합니다.
2. 백엔드가 돌려준 `access_token`을 Session Storage에 저장합니다.
3. Product 요청마다 `Authorization: Bearer <access_token>` 헤더를 보냅니다.
4. 로그아웃하면 Session Storage와 Streamlit 세션의 토큰을 삭제합니다.
