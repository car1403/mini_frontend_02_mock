# 아주 쉬운 실시간 데이터 설명

## 목표

```text
프론트엔드가 한 번 연결
        ↓
백엔드가 가상 온도 생성
        ↓
1초마다 SSE로 한 개씩 전송
        ↓
프론트엔드가 도착 즉시 화면 갱신
```

로그인, JWT, Supabase, Redis는 사용하지 않습니다.

## 일반 API와 SSE의 차이

일반 API:

```text
요청 → 응답 한 번 → 연결 종료
```

SSE:

```text
요청 → 데이터 1 → 데이터 2 → 데이터 3 → 연결 종료
```

## 가상 데이터

`app/services/real_service.py`가 다음 형태의 데이터를 만듭니다.

```json
{
  "number": 1,
  "temperature": 27,
  "status": "정상",
  "created_at": "10:30:05"
}
```

온도는 18℃부터 35℃ 사이에서 무작위로 생성됩니다.

## SSE 형식

```text
data: {"number": 1, "temperature": 27}

```

`data:` 뒤에 JSON을 적고 빈 줄을 넣으면 데이터 한 개가 완성됩니다.

## 코드 읽는 순서

1. `app/services/real_service.py`: 가상 데이터 생성
2. `app/schemes/real_scheme.py`: 데이터 모양 정의
3. `app/routers/real_router.py`: 1초마다 SSE 전송
4. `app/main.py`: 라우터 등록
5. `realtime/frontend/clients/real_client.py`: SSE 수신과 JSON 변환
6. `realtime/frontend/app.py`: 도착한 데이터를 화면에 표시

## 실행

터미널 1:

```powershell
cd realtime/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

터미널 2:

```powershell
cd realtime/frontend
pip install -r requirements.txt
streamlit run app.py
```

Streamlit 화면이 열리면 별도 버튼 없이 데이터 10개를 자동으로 받습니다.
