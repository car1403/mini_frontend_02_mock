# 프론트엔드 회원가입·로그인 실행

먼저 `backend_login_jwt_db/DB_GUIDE.md`를 따라 Supabase와 백엔드를 설정합니다.

```powershell
cd frontend_login_jwt_db
pip install -r requirements.txt
streamlit run app.py
```

사용 순서:

1. 회원가입 화면에서 새 계정을 만듭니다.
2. 로그인 화면에서 새 계정으로 로그인합니다.
3. 홈 화면에 Supabase에서 가져온 이름과 ID가 표시됩니다.
4. 로그인 후 Product와 Chat 기능을 사용할 수 있습니다.
