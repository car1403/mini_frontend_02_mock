# Mini Frontend 학습 예제

기본 프로젝트는 루트의 `backend`, `frontend`에 두고, 확장 예제는 기능별 폴더 아래 `backend`, `frontend`로 구성합니다.

## 프로젝트 구조

| 예제 | Backend | Frontend | 핵심 내용 |
|---|---|---|---|
| 기본 | `backend` | `frontend` | 기본 FastAPI와 Streamlit |
| 로그인 | `login/backend` | `login/frontend` | 간단한 로그인 |
| 로그인 Chat | `login_chat/backend` | `login_chat/frontend` | 메모리 세션과 Gemini Chat |
| DB 로그인 | `login_db/backend` | `login_db/frontend` | Supabase 회원가입과 로그인 |
| JWT 로그인 | `login_jwt/backend` | `login_jwt/frontend` | JWT와 Bearer 인증 |
| JWT DB 로그인 | `login_jwt_db/backend` | `login_jwt_db/frontend` | Supabase 회원가입과 JWT |
| JWT DB 로그인 + RLS | `login_jwt_db_rls/backend` | `login_jwt_db_rls/frontend` | JWT, DB, RLS |
| 가상 실시간 | `realtime/backend` | `realtime/frontend` | 가상 데이터와 SSE |
| 실제 실시간 | `realtime_data/backend` | `realtime_data/frontend` | Supabase, Redis, SSE |
| 실제 실시간 + JWT | `realtime_data_jwt/backend` | `realtime_data_jwt/frontend` | 실시간 데이터와 JWT |
| 단순 실시간 | `realtime_data_simple/backend` | `realtime_data_simple/frontend` | 단순화한 실시간 데이터 |
| 탭 UI | 없음 | `tab/frontend` | Streamlit 탭 구성 |

## 실행 방법

실행하려는 예제의 backend 폴더로 이동합니다.

```powershell
cd login_jwt\backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

새 터미널에서 같은 예제의 frontend 폴더로 이동합니다.

```powershell
cd login_jwt\frontend
pip install -r requirements.txt
streamlit run app.py
```

각 예제의 환경 변수, SQL, 실행 순서는 해당 폴더의 `README.md` 또는 가이드 문서를 참고하세요.
