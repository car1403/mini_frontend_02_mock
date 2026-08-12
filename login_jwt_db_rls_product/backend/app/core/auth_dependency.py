import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import create_client

from app.core.db_config import (
    SUPABASE_PUBLISHABLE_KEY,
    SUPABASE_URL,
    check_db_config,
)
from app.schemes.auth_scheme import CurrentUser


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    """Supabase Auth 토큰을 검증하고 현재 사용자의 DB 역할까지 조회합니다."""

    if credentials is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    token = credentials.credentials

    try:
        check_db_config()
        auth_client = create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)
        auth_response = auth_client.auth.get_user(token)
        user = auth_response.user

        if user is None:
            raise HTTPException(status_code=401, detail="사용자를 확인할 수 없습니다.")

        role_response = httpx.get(
            f"{SUPABASE_URL}/rest/v1/user_roles",
            params={"select": "role", "user_id": f"eq.{user.id}"},
            headers={
                "apikey": SUPABASE_PUBLISHABLE_KEY,
                "Authorization": f"Bearer {token}",
            },
            timeout=10.0,
        )
        role_response.raise_for_status()
        roles = role_response.json()

        if not roles:
            raise HTTPException(status_code=403, detail="사용자 역할이 없습니다.")

        return CurrentUser(
            user_id=str(user.id),
            email=user.email or "",
            role=roles[0]["role"],
            access_token=token,
        )
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail="토큰이 올바르지 않거나 만료되었습니다.",
        ) from error


def require_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """현재 사용자가 관리자가 아니면 Product 변경 요청을 차단합니다."""

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="관리자만 사용할 수 있는 기능입니다.",
        )

    return current_user
