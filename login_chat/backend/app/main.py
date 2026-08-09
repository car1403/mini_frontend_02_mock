from fastapi import FastAPI

import app.core.chat_config
from app.routers.auth_router import auth_router
from app.routers.chat_router import chat_router


app = FastAPI(
    title="로그인 후 Chat API",
    description="서버 메모리 세션으로 로그인한 사용자만 Chat을 이용하는 예제입니다.",
)

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/health")
def health():
    return {"status": "ok"}
