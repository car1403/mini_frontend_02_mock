# Supabase Auth + Product RLS 백엔드

Supabase Auth로 로그인하고 PostgreSQL RLS로 Product 권한을 제한하는 FastAPI 예제입니다.

## 권한

| 작업 | 일반 사용자 | 관리자 |
| --- | --- | --- |
| 상품 조회 | 가능 | 가능 |
| 상품 생성 | 불가 | 가능 |
| 상품 수정 | 불가 | 가능 |
| 상품 삭제 | 불가 | 가능 |

FastAPI가 먼저 역할을 확인하고, Supabase RLS가 DB에서 다시 권한을 확인합니다.
Product CRUD에서는 `service_role`을 사용하지 않습니다.

## 실행 순서

1. [DB_GUIDE.md](DB_GUIDE.md)를 따라 Supabase를 설정합니다.
2. `.env.example`을 `.env`로 복사하고 실제 값을 입력합니다.
3. 백엔드를 실행합니다.

```powershell
cd login_jwt_db_rls_product/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API 문서는 `http://127.0.0.1:8000/docs`에서 확인합니다.
