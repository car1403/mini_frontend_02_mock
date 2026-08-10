"""인증 API가 주고받는 데이터의 모양을 정의합니다."""

from pydantic import BaseModel


class AuthPublic(BaseModel):
    """비밀번호를 제외하고 외부에 보여 줄 사용자 정보입니다."""

    id: str
    name: str | None = None


class AuthLogin(BaseModel):
    """로그인 요청에서 받는 아이디와 비밀번호입니다."""

    id: str
    pwd: str


class TokenResponse(BaseModel):
    """로그인 성공 후 프론트엔드에 반환하는 JWT 응답입니다."""

    access_token: str
    # Authorization 헤더에서 사용하는 인증 방식이며 값은 bearer입니다.
    token_type: str
