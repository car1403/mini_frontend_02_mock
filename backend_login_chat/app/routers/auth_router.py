from fastapi import APIRouter, Header

from app.schemes.auth_scheme import AuthLogin, LoginResponse, LogoutResponse
from app.services.auth_service import login_process, logout_process


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=LoginResponse)
def login(auth: AuthLogin):
    return login_process(auth)


@auth_router.post("/logout", response_model=LogoutResponse)
def logout(
    session_token: str | None = Header(default=None, alias="X-Session-Token"),
):
    if session_token:
        return logout_process(session_token)
    return LogoutResponse(message="로그아웃되었습니다.")
