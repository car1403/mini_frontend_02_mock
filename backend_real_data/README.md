# Supabase + Upstash Redis 실시간 데이터

로그인과 JWT 없이 다음 흐름만 학습하는 백엔드입니다.

```text
센서 데이터 입력
→ Supabase 저장
→ Upstash Redis Publish
→ Redis Subscribe
→ SSE 전송
```

설정과 실행 방법은 [REALTIME_GUIDE.md](REALTIME_GUIDE.md)를 참고하세요.
