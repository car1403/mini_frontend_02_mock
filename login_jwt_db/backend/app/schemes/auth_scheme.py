from pydantic import BaseModel, Field


class AuthPublic(BaseModel):
    id: str
    name: str


class AuthSignup(BaseModel):
    id: str = Field(min_length=3, max_length=30)
    pwd: str = Field(min_length=4, max_length=100)
    name: str = Field(min_length=1, max_length=50)


class AuthLogin(BaseModel):
    id: str
    pwd: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: AuthPublic
