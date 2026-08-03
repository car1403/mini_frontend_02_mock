# Supabase + Upstash Redis 실시간 데이터

로그인과 JWT 없이 다음 흐름만 학습하는 백엔드입니다.

```text
센서 데이터 입력
→ Supabase 저장
→ Upstash Redis Publish
→ Redis Subscribe
→ SSE 전송
```

## 1. 외부 서비스 준비

Supabase SQL Editor에서 `schema.sql`을 실행하고 `.env.example`을 복사해 `.env`를 만듭니다.

```env
SUPABASE_URL=https://프로젝트ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=실제-service-role-key
REDIS_URL=rediss://default:비밀번호@호스트:6379
```

Upstash는 REST URL이 아닌 `rediss://` Redis Protocol URL을 사용합니다.

## 2. 실행

```powershell
cd backend_real_data_simple
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API 문서는 `http://127.0.0.1:8000/docs`에서 확인합니다.

| API | 역할 |
| --- | --- |
| `POST /real-data` | Supabase 저장 후 Redis 발행 |
| `GET /real-data/recent` | Supabase 최근 기록 조회 |
| `GET /real-data/stream` | Redis 이벤트 SSE 수신 |

`POST /real-data`의 `event_published`가 `false`이면 Supabase 저장은 성공했지만 Redis 발행은
실패한 것입니다. 이 경우 같은 데이터를 다시 입력하지 말고 `.env`의 `REDIS_URL`을 확인합니다.

## 3. 테스트

```powershell
pytest -q
```
