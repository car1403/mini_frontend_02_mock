from fastapi import FastAPI

from app.routers.real_router import real_router


app = FastAPI(
    title="아주 쉬운 가상 실시간 데이터 API",
    description="로그인 없이 가상 온도를 SSE로 전송하는 학습용 API입니다.",
)

app.include_router(real_router)


@app.get("/health")
def health():
    return {"status": "ok"}
