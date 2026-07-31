from fastapi import FastAPI
from app.routers.chat_router import chat_router
from app.routers.product_router import product_router
from app.routers.auth_router import auth_router
from app.routers.real_router import real_router
import app.core.chat_config  

tags_metadata = [
    {
        "name":"Chat",
        "description":"Gemini 연동"
    },
    {
        "name":"Product",
        "description":"Product 연동"        
    },
    {
        "name":"Auth",
        "description":"Login & Logout 연동"        
    },
    {
        "name": "Real Data",
        "description": "가상 온도 SSE 실시간 전송",
    },
]

app = FastAPI(title="Main App", openapi_tags=tags_metadata)

app.include_router(chat_router)
app.include_router(product_router)
app.include_router(auth_router)
app.include_router(real_router)
