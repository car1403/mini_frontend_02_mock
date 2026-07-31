from fastapi import APIRouter

from app.schemes.auth_scheme import AuthLogin, AuthPublic, TokenResponse
from app.services.auth_service import login_process, logout_process


auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/auth/login")
def login(auth: AuthLogin) -> TokenResponse:
    """로그인 성공 시 JWT를 발급합니다."""
    return login_process(auth)


@auth_router.get("/auth/logout/{id}")
def logout(id: str) -> AuthPublic:
    return logout_process(id)
