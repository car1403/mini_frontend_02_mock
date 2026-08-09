# 간단한 Supabase 회원가입과 로그인

## 1. 테이블 만들기

Supabase SQL Editor에서 `sql/customers.sql`을 실행합니다.

```sql
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    pwd TEXT NOT NULL,
    name TEXT NOT NULL
);
```

## 2. 환경 변수

`login_db/backend/.env` 파일을 만듭니다.

```env
SUPABASE_URL=https://프로젝트ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=실제-service-role-key
GEMINI_API_KEY=실제-Gemini-key
GEMINI_MODEL=gemini-2.5-flash-lite
```

## 3. 실행

```powershell
cd login_db/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 4. API

회원가입:

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

로그인:

```http
POST /auth/login
```

```json
{
  "id": "user01",
  "pwd": "password123"
}
```

비밀번호는 평문이 아니라 PBKDF2 해시로 `pwd` 컬럼에 저장됩니다.

이 버전은 DB 회원가입과 로그인까지만 다루며 JWT나 서버 세션은 사용하지 않습니다.
