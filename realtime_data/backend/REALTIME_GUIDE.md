# 로그인 없는 실제 실시간 데이터 가이드

## 역할

- Supabase: 센서 데이터 영구 저장과 최근 기록 조회
- Upstash Redis: 새 데이터 Publish/Subscribe
- SSE: Redis 메시지를 Streamlit으로 전달

로그인과 JWT는 사용하지 않습니다. JWT까지 결합한 버전은 `realtime_data_jwt/backend`에 있습니다.

## Supabase 테이블

Supabase SQL Editor에서 `schema.sql`을 실행합니다.

## 환경 변수

`realtime_data/backend/.env` 파일을 만듭니다.

```env
SUPABASE_URL=https://프로젝트ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=실제-service-role-key
REDIS_URL=rediss://default:비밀번호@호스트:6379
```

Upstash는 REST URL이 아니라 `rediss://`로 시작하는 Redis Protocol URL을 사용합니다.

## 실행

```powershell
cd realtime_data/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```powershell
cd realtime_data/frontend
pip install -r requirements.txt
streamlit run app.py
```

## 확인

1. 첫 번째 브라우저 탭에서 `2. 실시간 수신`을 시작합니다.
2. 두 번째 탭에서 `1. 센서 입력·조회`로 데이터를 입력합니다.
3. 데이터가 Supabase에 저장되고 Redis에 발행됩니다.
4. 첫 번째 탭이 SSE를 통해 새 데이터를 받습니다.

## API

- `POST /real-data`: Supabase 저장 후 Redis 발행
- `GET /real-data/recent`: Supabase 최근 기록 조회
- `GET /real-data/stream`: Redis 이벤트 SSE 수신
