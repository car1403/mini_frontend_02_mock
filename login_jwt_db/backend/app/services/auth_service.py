from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from supabase import Client, create_client

from app.core.db_config import (
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_URL,
    check_db_config,
)
from app.core.jwt_config import (
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)
from app.core.password import hash_password, verify_password
from app.schemes.auth_scheme import (
    AuthLogin,
    AuthPublic,
    AuthSignup,
    TokenResponse,
)


def get_supabase() -> Client:
    check_db_config()
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def signup_process(auth: AuthSignup) -> AuthPublic:
    try:
        client = get_supabase()
        existing = (
            client
            .table("customers")
            .select("id")
            .eq("id", auth.id)
            .limit(1)
            .execute()
        )

        if existing.data:
            raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")

        payload = {
            "id": auth.id,
            "pwd": hash_password(auth.pwd),
            "name": auth.name,
        }
        result = client.table("customers").insert(payload).execute()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="회원가입 DB 처리에 실패했습니다. Supabase 설정을 확인해 주세요.",
        )

    if not result.data:
        raise HTTPException(status_code=503, detail="회원가입 결과가 없습니다.")

    return AuthPublic(id=auth.id, name=auth.name)


def login_process(auth: AuthLogin) -> TokenResponse:
    try:
        result = (
            get_supabase()
            .table("customers")
            .select("id, pwd, name")
            .eq("id", auth.id)
            .limit(1)
            .execute()
        )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="로그인 DB 처리에 실패했습니다. Supabase 설정을 확인해 주세요.",
        )

    if not result.data:
        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )

    customer = result.data[0]

    if not verify_password(auth.pwd, customer["pwd"]):
        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )

    user = AuthPublic(id=customer["id"], name=customer["name"])
    return TokenResponse(
        access_token=create_access_token(customer["id"]),
        token_type="bearer",
        user=user,
    )


def logout_process(id: str) -> AuthPublic:
    return AuthPublic(id=id, name="")
