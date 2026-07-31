# 프론트엔드 실행 가이드

자세한 외부 서비스 설정은 `backend_real_data/REALTIME_GUIDE.md`를 먼저 확인하세요.

## 실행

```powershell
cd frontend_real_data
pip install -r requirements.txt
streamlit run app.py
```

## 사용 순서

1. `id01 / pwd01`로 로그인합니다.
2. 브라우저 탭 두 개를 엽니다.
3. 첫 번째 탭에서 `2. 실시간 수신`을 시작합니다.
4. 두 번째 탭에서 `1. 센서 데이터 입력·조회`로 데이터를 입력합니다.
5. 첫 번째 탭에 새 데이터가 표시되는지 확인합니다.
6. `Supabase 최근 데이터 조회`로 영구 저장된 데이터도 확인합니다.
