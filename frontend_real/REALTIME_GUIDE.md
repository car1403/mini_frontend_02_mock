# 프론트엔드 실시간 화면 사용법

## 실행

터미널 1:

```powershell
cd backend_real
pip install -r requirements.txt
uvicorn app.main:app --reload
```

터미널 2:

```powershell
cd frontend_real
pip install -r requirements.txt
streamlit run app.py
```

## 확인 순서

1. `id01 / pwd01`로 로그인합니다.
2. 왼쪽의 `실시간 온도` 메뉴를 선택합니다.
3. 받을 데이터 개수를 선택합니다.
4. `실시간 데이터 받기` 버튼을 누릅니다.
5. 온도 데이터가 1초마다 추가되는 모습을 확인합니다.

Supabase와 Redis는 필요하지 않습니다. 모든 데이터는 백엔드가 실행 중에 가상으로 만듭니다.
