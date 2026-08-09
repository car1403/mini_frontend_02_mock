from fastapi import APIRouter, status

from app.schemes.auth_scheme import (
    AuthLogin,
    AuthPublic,
    AuthSignup,
    TokenResponse,
)
from app.services.auth_service import (
    login_process,
    logout_process,
    signup_process,
)


auth_router = APIRouter(tags=["Auth"])


@auth_router.post(
    "/auth/signup",
    response_model=AuthPublic,
    status_code=status.HTTP_201_CREATED,
)
def signup(auth: AuthSignup):
    return signup_process(auth)


@auth_router.post("/auth/login", response_model=TokenResponse)
def login(auth: AuthLogin):
    return login_process(auth)


@auth_router.get("/auth/logout/{id}", response_model=AuthPublic)
def logout(id: str):
    return logout_process(id)
