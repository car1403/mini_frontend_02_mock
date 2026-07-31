# Supabase + Upstash Redis 실시간 데이터 초보자 가이드

## 1. 전체 구조

이 예제에서는 Supabase와 Upstash Redis를 모두 사용합니다.

```text
Streamlit에서 센서 데이터 입력
              ↓
FastAPI가 JWT 확인
              ↓
       Supabase에 저장
              ↓
   Upstash Redis에 publish
              ↓
 FastAPI SSE가 Redis subscribe
              ↓
 Streamlit 실시간 화면에 표시
```

두 서비스의 역할은 다릅니다.

| 서비스 | 역할 |
|---|---|
| Supabase | 데이터를 영구 저장하고 과거 데이터를 조회 |
| Upstash Redis | 새 데이터가 생겼다는 사실을 빠르게 전달 |
| SSE | Redis에서 받은 데이터를 프론트엔드로 계속 전송 |

## 2. Supabase 테이블 만들기

1. Supabase Dashboard에 로그인합니다.
2. 프로젝트를 선택합니다.
3. 왼쪽의 **SQL Editor**를 엽니다.
4. 이 폴더의 `schema.sql` 내용을 붙여 넣습니다.
5. **Run**을 누릅니다.

생성되는 테이블은 다음과 같습니다.

```text
realtime_sensor_data
```

저장되는 값:

- 장치 이름
- 온도
- 습도
- 데이터를 입력한 사용자 ID
- 입력 시간

## 3. Supabase 연결 값 확인

Supabase Project Settings의 API 설정에서 다음 값을 확인합니다.

```env
SUPABASE_URL=https://프로젝트ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=service_role_key
```

`service_role` 키는 강한 권한을 가지고 있습니다.

- 백엔드 `.env`에만 저장합니다.
- 프론트엔드에 넣으면 안 됩니다.
- GitHub에 올리면 안 됩니다.
- 다른 사람에게 보여 주면 안 됩니다.

## 4. Upstash Redis 만들기

1. Upstash Console에 로그인합니다.
2. Redis Database를 생성합니다.
3. Database 상세 화면에서 Redis 연결 정보를 엽니다.
4. `rediss://`로 시작하는 Redis Protocol URL을 복사합니다.

```env
REDIS_URL=rediss://default:비밀번호@호스트:6379
```

다음 REST 주소는 이 Pub/Sub 예제에서 사용하지 않습니다.

```text
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
```

이 예제는 Redis의 publish/subscribe 기능을 사용하므로 반드시 `rediss://` 형식의 주소가 필요합니다.

## 5. 환경 변수 만들기

`backend_real_data/.env.example`을 참고하여 같은 폴더에 `.env` 파일을 만듭니다.

```env
SUPABASE_URL=https://프로젝트ID.supabase.co
SUPABASE_SERVICE_ROLE_KEY=실제-service-role-key
REDIS_URL=rediss://default:비밀번호@호스트:6379
JWT_SECRET_KEY=길고-복잡한-임의의-문자열
```

## 6. 실행

터미널 1:

```powershell
cd backend_real_data
pip install -r requirements.txt
uvicorn app.main:app --reload
```

터미널 2:

```powershell
cd frontend_real_data
pip install -r requirements.txt
streamlit run app.py
```

로그인 정보:

```text
ID: id01
PWD: pwd01
```

## 7. 화면 확인 순서

브라우저 탭을 두 개 사용하면 이해하기 쉽습니다.

첫 번째 탭:

1. 로그인합니다.
2. `2. 실시간 수신`을 엽니다.
3. `실시간 수신 시작`을 누릅니다.

두 번째 탭:

1. 같은 Streamlit 주소를 엽니다.
2. `1. 센서 데이터 입력·조회`를 엽니다.
3. 온도와 습도를 입력합니다.
4. `Supabase 저장 + Redis 발행`을 누릅니다.

첫 번째 탭의 표에 새 데이터가 바로 나타납니다.

## 8. API 처리 과정

### POST /real-data

```text
JWT 검사
  ↓
Supabase insert
  ↓
Redis publish
  ↓
저장 결과 반환
```

### GET /real-data/recent

```text
JWT 검사
  ↓
Supabase select
  ↓
최근 데이터 반환
```

### GET /real-data/stream

```text
JWT 검사
  ↓
Redis subscribe
  ↓
새 메시지를 SSE로 전송
```

## 9. 코드 읽는 순서

1. `schema.sql`: Supabase 테이블 구조
2. `app/core/real_config.py`: Supabase와 Redis 환경 변수
3. `app/schemes/real_scheme.py`: 요청과 응답 데이터 모양
4. `app/services/real_service.py`: Supabase 저장과 Redis Pub/Sub
5. `app/routers/real_router.py`: REST API와 SSE
6. `frontend_real_data/clients/real_client.py`: API와 SSE 호출
7. `frontend_real_data/app_pages/real_input.py`: 입력과 과거 조회
8. `frontend_real_data/app_pages/real_stream.py`: 새 데이터 실시간 수신

## 10. 알아둘 점

Redis Pub/Sub 메시지는 과거 기록을 보관하지 않습니다.

실시간 화면에 연결하지 않은 동안 발생한 데이터는 Redis에서 다시 받을 수 없습니다. 하지만 같은 데이터가 Supabase에 저장되어 있으므로 `최근 데이터 조회`로 확인할 수 있습니다.

```text
과거 기록이 필요함 → Supabase 조회
지금 발생한 데이터 → Redis + SSE 수신
```

Supabase 저장 후 Redis 발행에 실패할 수도 있습니다. 이 경우 데이터는 Supabase에 남아 있지만 실시간 화면에는 전달되지 않습니다. 프론트엔드에는 두 작업 중 어느 부분이 실패했는지 메시지가 표시됩니다.
