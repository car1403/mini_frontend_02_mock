# 초보자를 위한 로그인 세션 Chat

## JWT를 사용하지 않는 이유

이 예제는 기존 `backend_login`을 기반으로 로그인 후 Chat을 사용하는 가장 단순한 흐름을 보여 줍니다.

JWT 대신 백엔드가 임의의 세션 토큰을 만들고 메모리에 저장합니다.

## 로그인

```http
POST /auth/login
```

```json
{
  "id": "id01",
  "pwd": "pwd01"
}
```

응답:

```json
{
  "session_token": "임의로 생성된 값",
  "user": {
    "id": "id01",
    "name": "이말숙"
  }
}
```

백엔드에는 다음과 비슷하게 저장됩니다.

```python
sessions[session_token] = user
```

## Chat

프론트는 질문과 세션 토큰을 보냅니다.

```http
POST /chat/gemini
X-Session-Token: 로그인할_때_받은_세션_토큰
```

```json
{
  "prompt": "안녕하세요"
}
```

사용자 ID는 요청 Body에 넣지 않습니다. 백엔드가 세션에서 사용자 ID를 확인해 Chat 서비스에 전달합니다.

## 로그아웃

```http
POST /auth/logout
X-Session-Token: 세션_토큰
```

백엔드는 메모리에서 해당 세션을 삭제합니다.

## 주의

이 세션은 학습용 메모리 세션입니다.

- 서버를 재시작하면 모든 세션이 사라집니다.
- 여러 서버를 동시에 실행하면 세션을 공유하지 못합니다.
- 실제 서비스에서는 Redis나 DB 기반 세션을 사용할 수 있습니다.
