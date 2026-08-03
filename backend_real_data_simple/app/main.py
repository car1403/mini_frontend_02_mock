from fastapi import FastAPI

from app.routers.real_router import real_router


app = FastAPI(
    title="Supabase + Redis 실시간 데이터 API",
    description="로그인 없이 실제 DB 저장과 SSE 수신을 학습하는 예제입니다.",
)

app.include_router(real_router)


@app.get("/health")
def health():
    return {"status": "ok"}
