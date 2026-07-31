from pydantic import BaseModel


class AuthPublic(BaseModel):
    id: str
    name: str | None = None


class AuthLogin(BaseModel):
    id: str
    pwd: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
