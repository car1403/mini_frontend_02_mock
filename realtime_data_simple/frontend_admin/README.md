# 관리자 프론트엔드

관리자가 센서 데이터를 입력하고 Supabase의 최근 저장 데이터를 조회하는 Streamlit 앱입니다.
입력한 데이터는 백엔드를 통해 Redis 채널에도 발행됩니다.

## 실행

백엔드를 먼저 실행한 다음 새 터미널에서 실행합니다.

```powershell
cd realtime_data_simple/frontend_admin
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

브라우저에서 `http://127.0.0.1:8501`을 엽니다.
