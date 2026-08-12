from fastapi import FastAPI
from app.routers.chat_router import chat_router
from app.routers.product_router import product_router
from app.routers.auth_router import auth_router
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
]

app = FastAPI(title="Supabase Auth + Product RLS", openapi_tags=tags_metadata)

app.include_router(chat_router)
app.include_router(product_router)
app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}
