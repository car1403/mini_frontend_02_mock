# JWT 실시간 데이터 프론트엔드

먼저 `realtime_data_jwt/backend/REALTIME_GUIDE.md`를 따라 백엔드를 설정합니다.

```powershell
cd realtime_data_jwt/frontend
pip install -r requirements.txt
streamlit run app.py
```

1. `id01 / pwd01`로 로그인합니다.
2. 첫 번째 탭에서 실시간 수신을 시작합니다.
3. 두 번째 탭에서 센서 데이터를 입력합니다.
4. JWT로 인증된 SSE 화면에서 새 데이터를 확인합니다.
