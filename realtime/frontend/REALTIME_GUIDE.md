# 프론트엔드 자동 수신 가이드

## 실행 순서

터미널 1:

```powershell
cd realtime/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

터미널 2:

```powershell
cd realtime/frontend
pip install -r requirements.txt
streamlit run app.py
```

## 화면 동작

```text
Streamlit 화면 열림
       ↓
GET /real/stream?count=10 자동 연결
       ↓
가상 온도 1개 도착
       ↓
온도 카드와 표 갱신
       ↓
총 10개를 받으면 종료
```

회원가입, 로그인, JWT, Supabase, Redis 설정은 필요하지 않습니다.
