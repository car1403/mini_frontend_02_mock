from fastapi import Header, HTTPException

from app.schemes.auth_scheme import AuthPublic
from app.services.auth_service import find_session_user


def get_current_user(
    session_token: str | None = Header(default=None, alias="X-Session-Token"),
) -> AuthPublic:
    if not session_token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    user = find_session_user(session_token)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="세션이 없거나 만료되었습니다. 다시 로그인해 주세요.",
        )
    return user
