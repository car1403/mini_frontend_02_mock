# 사용자 프론트엔드

사용자가 Redis와 SSE를 통해 전달되는 센서 데이터를 실시간으로 확인하는 Streamlit 앱입니다.

## 실행

백엔드를 먼저 실행한 다음 새 터미널에서 실행합니다.

```powershell
cd realtime_data_simple/frontend_user
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py --server.port 8502
```

브라우저에서 `http://127.0.0.1:8502`를 엽니다.
