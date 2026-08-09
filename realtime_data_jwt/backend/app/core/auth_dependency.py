import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.jwt_config import JWT_ALGORITHM, JWT_SECRET_KEY


# Swagger 문서에 Authorize 버튼을 만들어 줍니다.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="사용자 정보가 없는 토큰입니다.")

        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰 사용 시간이 만료되었습니다.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="올바르지 않은 토큰입니다.")
