# Supabase 회원가입·로그인 초보자 가이드

## 전체 흐름

```text
회원가입 화면
   ↓
FastAPI /auth/signup
   ↓
비밀번호 해시 처리
   ↓
Supabase customers 저장

로그인 화면
   ↓
FastAPI /auth/login
   ↓
Supabase에서 ID 조회
   ↓
비밀번호 해시 비교
   ↓
JWT 발급
```

프론트엔드는 Supabase에 직접 연결하지 않습니다. Supabase의 강한 권한을 가진 `service_role` 키는 백엔드만 사용합니다.

## 1. 테이블 만들기

Supabase Dashboard의 SQL Editor에서 `schema.sql`을 실행합니다.

```sql
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    pwd TEXT NOT NULL,
    name TEXT NOT NULL
);
```

이 폴더는 초보자가 회원가입, DB 로그인, JWT 발급 흐름에 집중할 수 있도록 RLS를 사용하지 않습니다.

RLS까지 적용한 다음 단계 예제는 `login_jwt_db_rls/backend` 폴더에 있습니다.

## 2. 환경 변수 만들기

`login_jwt_db/backend` 폴더에 `.env` 파일을 만듭니다.

```env
SUPABASE_URL=https://프로젝트ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=실제-service-role-key
JWT_SECRET_KEY=길고-복잡한-임의의-문자열
```

Supabase URL과 service role key는 Supabase Project Settings의 API 설정에서 확인할 수 있습니다.

`SUPABASE_SERVICE_ROLE_KEY`는 frontend나 GitHub에 절대 공개하면 안 됩니다.

RLS를 사용하지 않는 버전이므로 특히 다음 원칙을 지켜야 합니다.

- frontend에서 Supabase를 직접 호출하지 않습니다.
- 모든 DB 요청은 FastAPI backend를 거칩니다.
- service role key는 backend의 `.env`에만 저장합니다.

## 3. 회원가입

요청:

```http
POST /auth/signup
```

```json
{
  "id": "user01",
  "pwd": "password123",
  "name": "홍길동"
}
```

백엔드는 다음 순서로 처리합니다.

1. 같은 ID가 있는지 조회합니다.
2. 비밀번호를 PBKDF2 방식으로 해시합니다.
3. ID, 비밀번호 해시, 이름을 customers에 저장합니다.

DB의 `pwd`에는 입력한 비밀번호가 그대로 저장되지 않습니다.

```text
입력: password123
저장: pbkdf2_sha256$200000$...$...
```

해시는 원래 비밀번호로 되돌리는 암호화가 아닙니다. 로그인할 때 입력값을 다시 해시하여 DB 값과 비교합니다.

## 4. 로그인

요청:

```http
POST /auth/login
```

```json
{
  "id": "user01",
  "pwd": "password123"
}
```

로그인에 성공하면 JWT와 DB의 사용자 정보를 반환합니다.

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "user01",
    "name": "홍길동"
  }
}
```

JWT의 `sub`에는 DB에서 확인된 사용자 ID가 들어갑니다.

## 5. 실행

터미널 1:

```powershell
cd login_jwt_db/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

터미널 2:

```powershell
cd login_jwt_db/frontend
pip install -r requirements.txt
streamlit run app.py
```

## 6. 확인 순서

1. Streamlit의 회원가입 메뉴를 엽니다.
2. ID, 비밀번호, 이름을 입력합니다.
3. Supabase Table Editor에서 customers 행을 확인합니다.
4. `pwd`가 평문이 아닌 해시인지 확인합니다.
5. 로그인 메뉴에서 새 계정으로 로그인합니다.
6. 홈 화면에 DB에서 읽은 이름과 ID가 표시되는지 확인합니다.
7. Product와 Chat API가 발급된 JWT로 동작하는지 확인합니다.

## 주요 파일

| 파일 | 역할 |
|---|---|
| `schema.sql` | customers 테이블 생성 |
| `app/core/db_config.py` | Supabase 환경 변수 |
| `app/core/password.py` | 비밀번호 해시와 비교 |
| `app/services/auth_service.py` | 회원가입, DB 로그인, JWT 발급 |
| `app/routers/auth_router.py` | signup과 login API |
| `login_jwt_db/frontend/app_pages/02_signup.py` | 회원가입 화면 |
| `login_jwt_db/frontend/core/auth.py` | 로그인 결과와 JWT 보관 |
