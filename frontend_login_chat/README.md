# 로그인 후 이용하는 AI Chat 화면

로그인하지 않으면 Chat 메뉴가 보이지 않고, 로그인한 사용자만 Gemini와 대화할 수 있습니다.

## 실행

백엔드를 먼저 실행한 후:

```powershell
cd frontend_login_chat
pip install -r requirements.txt
streamlit run app.py
```

학습용 로그인 정보:

```text
ID: id01
PWD: pwd01
```

화면 구성:

- 로그인 전: 홈, 로그인
- 로그인 후: 홈, AI Chat, 로그아웃
- AI Chat: 사용자와 Gemini 메시지를 대화 형태로 표시
