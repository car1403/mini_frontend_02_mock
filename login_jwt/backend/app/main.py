"""FastAPI 앱을 만들고 각 기능의 라우터를 등록하는 시작 파일입니다."""

from fastapi import FastAPI
from app.routers.chat_router import chat_router
from app.routers.product_router import product_router
from app.routers.auth_router import auth_router
import app.core.chat_config  

# Swagger 문서(/docs)에 표시할 API 그룹 이름과 설명입니다.
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
]

# FastAPI 애플리케이션 객체를 생성합니다.
app = FastAPI(title="Main App", openapi_tags=tags_metadata)

# 각 라우터를 등록해야 해당 파일에 작성한 URL을 실제로 호출할 수 있습니다.
app.include_router(chat_router)
app.include_router(product_router)
app.include_router(auth_router)
