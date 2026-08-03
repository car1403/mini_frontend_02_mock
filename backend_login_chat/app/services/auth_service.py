import secrets

from fastapi import HTTPException

from app.schemes.auth_scheme import (
    AuthLogin,
    AuthPublic,
    LoginResponse,
    LogoutResponse,
)


# 학습용 서버 메모리 세션입니다. 서버를 종료하면 모두 사라집니다.
sessions: dict[str, AuthPublic] = {}


def login_process(auth: AuthLogin) -> LoginResponse:
    if auth.id != "id01" or auth.pwd != "pwd01":
        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )

    user = AuthPublic(id=auth.id, name="이말숙")
    session_token = secrets.token_urlsafe(32)
    sessions[session_token] = user
    return LoginResponse(session_token=session_token, user=user)


def find_session_user(session_token: str) -> AuthPublic | None:
    return sessions.get(session_token)


def logout_process(session_token: str) -> LogoutResponse:
    sessions.pop(session_token, None)
    return LogoutResponse(message="로그아웃되었습니다.")
