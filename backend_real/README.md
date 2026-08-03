# 아주 쉬운 SSE 실시간 백엔드

로그인, JWT, DB, Redis 없이 가상 온도를 SSE로 보내는 FastAPI 예제입니다.

## 실행

```powershell
cd backend_real
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## API

- `GET /health`: 서버 확인
- `GET /real/one`: 가상 온도 한 개
- `GET /real/stream?count=10`: 가상 온도 10개를 1초 간격으로 SSE 전송

자세한 설명은 [REALTIME_GUIDE.md](REALTIME_GUIDE.md)를 참고하세요.
