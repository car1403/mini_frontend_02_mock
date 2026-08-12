from typing import Literal

from pydantic import BaseModel, Field


AppRole = Literal["user", "admin"]


class AuthPublic(BaseModel):
    """프론트엔드에 공개해도 되는 로그인 사용자 정보입니다."""

    id: str
    email: str
    name: str
    role: AppRole = "user"


class AuthSignup(BaseModel):
    """Supabase Auth 회원가입에 필요한 이메일, 비밀번호, 이름입니다."""

    email: str = Field(min_length=5, max_length=200)
    pwd: str = Field(min_length=6, max_length=100)
    name: str = Field(min_length=1, max_length=50)


class AuthLogin(BaseModel):
    email: str
    pwd: str


class TokenResponse(BaseModel):
    """Supabase Auth 로그인 성공 후 반환하는 사용자 Access Token입니다."""

    access_token: str
    token_type: str
    user: AuthPublic


class CurrentUser(BaseModel):
    """백엔드가 검증한 현재 사용자와 원본 Access Token입니다."""

    user_id: str
    email: str
    role: AppRole
    access_token: str
