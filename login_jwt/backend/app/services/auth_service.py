"""로그인 확인과 JWT 생성 등 인증의 실제 처리를 담당합니다."""

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
    """사용자 ID와 만료 시간을 담은 JWT 문자열을 만듭니다."""

    # 서버마다 시간대가 달라도 동일하게 계산되도록 UTC 현재 시간을 사용합니다.
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        # sub에는 이 토큰의 주인인 사용자 ID를 넣습니다.
        "sub": user_id,
        # exp가 지나면 jwt.decode()에서 만료된 토큰으로 판단합니다.
        "exp": expire,
    }
    # payload에 비밀키로 서명하여 위조 여부를 확인할 수 있는 JWT를 만듭니다.
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def login_process(auth: AuthLogin) -> TokenResponse:
    """아이디와 비밀번호를 확인하고 성공하면 JWT를 반환합니다."""

    # 학습용 예제라서 DB 대신 정해진 계정과 비교합니다.
    if auth.id == "id01" and auth.pwd == "pwd01":
        token = create_access_token(auth.id)
        return TokenResponse(access_token=token, token_type="bearer")

    raise HTTPException(
        status_code=401,
        detail="아이디 또는 비밀번호가 올바르지 않습니다.",
    )


def logout_process(id: str) -> AuthPublic:
    """로그아웃할 사용자의 공개 정보를 반환합니다."""

    # JWT 로그아웃은 클라이언트가 저장한 토큰을 지우는 방식으로 처리합니다.
    # 서버가 토큰을 저장하지 않기 때문에 여기서는 별도로 삭제할 데이터가 없습니다.
    return AuthPublic(id=id)
