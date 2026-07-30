# chat_service.py

from fastapi import HTTPException

from app.schemes.auth_scheme import AuthLogin, AuthPublic

def login_process(auth: AuthLogin)-> AuthPublic:
    if(auth.id == "id01" and auth.pwd == "pwd01"):
        return AuthPublic(
            id = auth.id,
            name = "이말숙"
        )
    else:
        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )

def logout_process(id: str)-> AuthPublic:
    
    return AuthPublic(
        id = id
    )