# 아주 쉬운 실시간 데이터 설명

## 이 예제의 목표

복잡한 데이터베이스나 Redis 없이 다음 흐름만 먼저 연습합니다.

```text
프론트엔드가 연결
        ↓
백엔드가 가상 온도 생성
        ↓
백엔드가 1초마다 한 개씩 전송
        ↓
프론트엔드가 받자마자 화면 갱신
```

백엔드가 데이터를 계속 보내는 방식으로 SSE(Server-Sent Events)를 사용합니다.

## SSE란?

일반적인 API는 요청 한 번에 응답 한 번을 반환합니다.

```text
요청 → 응답 → 연결 종료
```

SSE는 한 번 연결한 후 서버가 여러 응답을 연속해서 보냅니다.

```text
요청 → 데이터 1 → 데이터 2 → 데이터 3 → 연결 종료
```

이 예제는 이해하기 쉽도록 사용자가 선택한 개수만큼 전송한 후 연결을 종료합니다.

## 가상 데이터

`app/services/real_service.py`는 DB 대신 다음 데이터를 만듭니다.

```json
{
  "number": 1,
  "temperature": 27,
  "status": "정상",
  "created_at": "10:30:05"
}
```

온도는 18도부터 35도 사이에서 무작위로 만들어집니다.

## SSE 데이터 형식

서버는 한 데이터를 다음 문자열로 보냅니다.

```text
data: {"number": 1, "temperature": 27}

```

`data:` 뒤에 JSON을 적고 마지막에 빈 줄을 하나 넣습니다.
빈 줄은 하나의 데이터가 끝났다는 표시입니다.

## API

- `GET /real/one`: 가상 데이터 한 개 받기
- `GET /real/stream?count=10`: 1초마다 총 10개 받기

두 API 모두 로그인 후 발급된 JWT가 필요합니다.

## 코드 읽는 순서

1. `app/services/real_service.py`: 가상 데이터를 만듭니다.
2. `app/routers/real_router.py`: 가상 데이터를 SSE로 계속 보냅니다.
3. `frontend_real/clients/real_client.py`: SSE 문자열을 JSON으로 바꿉니다.
4. `frontend_real/app_pages/real_data.py`: 받은 데이터를 즉시 화면에 표시합니다.

## 기존 실습과 차이

기존 실습은 Supabase, Redis, Queue, SSE를 함께 사용합니다.

이 예제에서는 처음 이해해야 할 SSE 흐름만 남겼습니다.

```text
현재 예제: 가상 데이터 생성 → SSE → 화면
기존 실습: DB 저장 → Redis 발행 → Queue 구독 → SSE → 화면
```

현재 예제를 이해한 후 가상 데이터 생성 부분을 DB나 Redis로 교체하면 됩니다.
