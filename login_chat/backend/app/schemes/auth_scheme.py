from pydantic import BaseModel


class AuthLogin(BaseModel):
    id: str
    pwd: str


class AuthPublic(BaseModel):
    id: str
    name: str


class LoginResponse(BaseModel):
    session_token: str
    user: AuthPublic


class LogoutResponse(BaseModel):
    message: str
