from fastapi import APIRouter, status
from app.schemes.auth_scheme import AuthCreate, AuthLogin, AuthPublic
from app.services.auth_service import login_process, logout_process, signup_process

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/signup", response_model=AuthPublic, status_code=status.HTTP_201_CREATED)
def signup(auth: AuthCreate):
    return signup_process(auth)

@auth_router.post("/login", response_model=AuthPublic)
def login(auth: AuthLogin):
    return login_process(auth)

@auth_router.get("/logout/{customer_id}", response_model=AuthPublic)
def logout(customer_id: str):
    return logout_process(customer_id)
