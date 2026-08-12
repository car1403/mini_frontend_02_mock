import httpx
from fastapi import HTTPException
from supabase import Client, create_client

from app.core.db_config import (
    SUPABASE_PUBLISHABLE_KEY,
    SUPABASE_URL,
    check_db_config,
)
from app.schemes.auth_scheme import AuthLogin, AuthPublic, AuthSignup, TokenResponse


def get_supabase_auth() -> Client:
    """RLS를 우회하지 않는 publishable key로 Supabase Auth 클라이언트를 만듭니다."""

    check_db_config()
    return create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)


def get_user_data(access_token: str, user_id: str) -> tuple[str, str]:
    """사용자 토큰으로 자신의 프로필 이름과 역할을 RLS를 거쳐 조회합니다."""

    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
    }

    profile_response = httpx.get(
        f"{SUPABASE_URL}/rest/v1/user_profiles",
        params={"select": "name", "user_id": f"eq.{user_id}"},
        headers=headers,
        timeout=10.0,
    )
    role_response = httpx.get(
        f"{SUPABASE_URL}/rest/v1/user_roles",
        params={"select": "role", "user_id": f"eq.{user_id}"},
        headers=headers,
        timeout=10.0,
    )

    profile_response.raise_for_status()
    role_response.raise_for_status()

    profiles = profile_response.json()
    roles = role_response.json()

    if not profiles or not roles:
        raise RuntimeError("사용자 프로필 또는 역할을 찾을 수 없습니다.")

    return profiles[0]["name"], roles[0]["role"]


def signup_process(auth: AuthSignup) -> AuthPublic:
    """Supabase Auth에 가입하고 트리거로 생성된 일반 사용자 정보를 반환합니다."""

    try:
        response = get_supabase_auth().auth.sign_up(
            {
                "email": auth.email,
                "password": auth.pwd,
                "options": {"data": {"name": auth.name}},
            }
        )
    except Exception as error:
        raise HTTPException(
            status_code=409,
            detail="회원가입에 실패했습니다. 이미 가입한 이메일인지 확인해 주세요.",
        ) from error

    if response.user is None:
        raise HTTPException(status_code=503, detail="회원가입 사용자 정보가 없습니다.")

    return AuthPublic(
        id=str(response.user.id),
        email=response.user.email or auth.email,
        name=auth.name,
        role="user",
    )


def login_process(auth: AuthLogin) -> TokenResponse:
    """Supabase Auth로 로그인하고 Access Token과 DB 역할을 반환합니다."""

    try:
        response = get_supabase_auth().auth.sign_in_with_password(
            {"email": auth.email, "password": auth.pwd}
        )
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        ) from error

    if response.user is None or response.session is None:
        raise HTTPException(status_code=401, detail="로그인 세션을 만들 수 없습니다.")

    access_token = response.session.access_token
    user_id = str(response.user.id)

    try:
        name, role = get_user_data(access_token, user_id)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="사용자 프로필과 역할을 조회하지 못했습니다.",
        ) from error

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=AuthPublic(
            id=user_id,
            email=response.user.email or auth.email,
            name=name,
            role=role,
        ),
    )


def logout_process(user_id: str) -> dict[str, str]:
    """현재 예제는 프론트엔드가 토큰을 삭제하는 방식으로 로그아웃합니다."""

    return {"id": user_id}
