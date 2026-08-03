# 로그인 없는 실제 실시간 데이터 화면

회원가입과 JWT 없이 센서 데이터 입력·조회와 Redis SSE 수신만 보여 주는 Streamlit 예제입니다.

## 실행

먼저 `backend_real_data_simple`을 실행한 후 새 터미널에서 다음 명령을 실행합니다.

```powershell
cd frontend_real_data_simple
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## 확인 순서

1. `2. 실시간 수신` 화면에서 수신을 시작합니다.
2. 다른 브라우저 탭의 `1. 센서 입력·조회` 화면에서 데이터를 입력합니다.
3. 첫 번째 화면에 새 센서 데이터가 표시되는지 확인합니다.

입력 데이터는 Supabase에 저장된 후 Redis로 발행됩니다. Redis 발행만 실패한 경우에는
데이터를 다시 저장하지 않도록 저장 성공과 발행 실패를 따로 안내합니다.
