# JWT가 포함된 실제 실시간 데이터 가이드

```text
JWT 로그인
→ 센서 데이터 입력
→ Supabase realtime_sensor_data_jwt 저장
→ Upstash Redis Publish
→ Redis Subscribe
→ JWT로 보호된 SSE 전송
```

`realtime_data_jwt/backend/.env`:

```env
SUPABASE_URL=https://프로젝트ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=실제-service-role-key
REDIS_URL=rediss://default:비밀번호@호스트:6379
JWT_SECRET_KEY=길고-복잡한-임의의-문자열
```

Supabase SQL Editor에서 이 폴더의 `schema.sql`을 실행합니다.

```powershell
cd realtime_data_jwt/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```powershell
cd realtime_data_jwt/frontend
pip install -r requirements.txt
streamlit run app.py
```

`id01 / pwd01`로 로그인한 후 센서 입력과 실시간 수신 메뉴를 사용합니다.
