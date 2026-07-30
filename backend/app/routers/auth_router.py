# product_router.py

from fastapi import APIRouter
from app.schemes.auth_scheme import AuthPublic, AuthLogin
from app.services.auth_service import (
    login_process,
    logout_process
)

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/auth/login")
def login(auth: AuthLogin) -> AuthPublic:
    """Login"""
    return login_process(auth)

@auth_router.get("/auth/logout/{id}")
def logout(id:str) -> AuthPublic:
    return logout_process(id)
