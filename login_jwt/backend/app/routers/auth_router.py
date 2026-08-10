"""로그인과 로그아웃 URL을 정의하는 라우터입니다."""

from fastapi import APIRouter

from app.schemes.auth_scheme import AuthLogin, AuthPublic, TokenResponse
from app.services.auth_service import login_process, logout_process


auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/auth/login")
def login(auth: AuthLogin) -> TokenResponse:
    """로그인 성공 시 JWT를 발급합니다."""

    # 실제 로그인 판단과 JWT 생성은 서비스 함수에 맡깁니다.
    return login_process(auth)


@auth_router.get("/auth/logout/{id}")
def logout(id: str) -> AuthPublic:
    """로그아웃할 사용자 정보를 반환합니다."""

    return logout_process(id)
