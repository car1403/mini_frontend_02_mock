from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

from app.core.jwt_config import (
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)
from app.schemes.auth_scheme import AuthLogin, AuthPublic, TokenResponse


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def login_process(auth: AuthLogin) -> TokenResponse:
    if auth.id == "id01" and auth.pwd == "pwd01":
        token = create_access_token(auth.id)
        return TokenResponse(access_token=token, token_type="bearer")

    raise HTTPException(
        status_code=401,
        detail="아이디 또는 비밀번호가 올바르지 않습니다.",
    )


def logout_process(id: str) -> AuthPublic:
    # JWT 로그아웃은 클라이언트가 저장한 토큰을 지우는 방식으로 처리합니다.
    return AuthPublic(id=id)
