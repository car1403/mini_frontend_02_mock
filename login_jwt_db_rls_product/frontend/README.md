# Product RLS 프론트엔드

로그인 사용자의 DB 역할에 따라 Product 화면을 다르게 보여 주는 Streamlit 앱입니다.

- 일반 사용자: 상품 조회
- 관리자: 상품 조회·생성·수정·삭제

## 실행

```powershell
cd login_jwt_db_rls_product/frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

먼저 백엔드를 `http://127.0.0.1:8000`에서 실행해야 합니다.
