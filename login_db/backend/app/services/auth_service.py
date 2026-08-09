from fastapi import HTTPException
from app.core.password import hash_password, verify_password
from app.core.supabase_client import get_supabase
from app.schemes.auth_scheme import AuthCreate, AuthLogin, AuthPublic

def customer_get(customer_id: str) -> dict | None:
    result = get_supabase().table("customers").select("id, pwd, name").eq("id", customer_id).limit(1).execute()
    return result.data[0] if result.data else None

def signup_process(auth: AuthCreate) -> AuthPublic:
    try:
        if customer_get(auth.id):
            raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")
        result = get_supabase().table("customers").insert({"id": auth.id, "pwd": hash_password(auth.pwd), "name": auth.name}).execute()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=503, detail="회원가입 DB 처리에 실패했습니다.")
    if not result.data:
        raise HTTPException(status_code=503, detail="회원가입 결과가 없습니다.")
    return AuthPublic(id=auth.id, name=auth.name)

def login_process(auth: AuthLogin) -> AuthPublic:
    try:
        customer = customer_get(auth.id)
    except Exception:
        raise HTTPException(status_code=503, detail="로그인 DB 처리에 실패했습니다.")
    if customer is None or not verify_password(auth.pwd, customer["pwd"]):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다.")
    return AuthPublic(id=customer["id"], name=customer["name"])

def logout_process(customer_id: str) -> AuthPublic:
    return AuthPublic(id=customer_id, name="")
