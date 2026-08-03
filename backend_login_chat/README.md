# 로그인 후 이용하는 Chat 백엔드

JWT 대신 가장 단순한 서버 메모리 세션을 사용합니다.

```text
로그인
→ session_token 발급
→ 백엔드 메모리에 세션 저장
→ Chat 요청에 X-Session-Token 전달
→ 세션 사용자 확인
→ Gemini 호출
```

## 환경 변수

`.env.example`을 참고하여 `.env`를 만듭니다.

```env
GEMINI_API_KEY=실제-Gemini-API-key
GEMINI_MODEL=gemini-2.5-flash-lite
```

## 실행

```powershell
cd backend_login_chat
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger는 `http://127.0.0.1:8000/docs`에서 확인할 수 있습니다.

자세한 흐름은 [SESSION_CHAT_GUIDE.md](SESSION_CHAT_GUIDE.md)를 참고하세요.
