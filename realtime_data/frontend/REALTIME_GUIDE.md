# 프론트엔드 실행

먼저 `realtime_data/backend/REALTIME_GUIDE.md`를 따라 Supabase, Upstash, 백엔드를 설정합니다.

```powershell
cd realtime_data/frontend
pip install -r requirements.txt
streamlit run app.py
```

- `1. 센서 입력·조회`: DB 저장, Redis 발행, 최근 기록 조회
- `2. 실시간 수신`: Redis에 새로 발행된 데이터를 SSE로 수신

로그인이나 JWT는 필요하지 않습니다.
