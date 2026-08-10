"""요청에 포함된 JWT를 검사하고 현재 사용자 ID를 알아내는 파일입니다."""

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.jwt_config import JWT_ALGORITHM, JWT_SECRET_KEY


# Swagger 문서에 Authorize 버튼을 만들어 줍니다.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Authorization 헤더의 JWT를 검증하고 로그인한 사용자 ID를 반환합니다."""

    # Authorization 헤더가 없으면 로그인하지 않은 요청이므로 401을 반환합니다.
    if credentials is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    # "Bearer 실제토큰" 중 실제 토큰 문자열만 꺼냅니다.
    token = credentials.credentials

    try:
        # 비밀키와 알고리즘으로 서명을 확인하고 JWT 내용을 딕셔너리로 풉니다.
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        # sub(subject)는 이 토큰의 사용자가 누구인지 나타내는 표준 항목입니다.
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="사용자 정보가 없는 토큰입니다.")

        # 이 반환값은 Depends(get_current_user)를 사용한 API의 current_user에 들어갑니다.
        return user_id
    except jwt.ExpiredSignatureError:
        # exp 시간이 지난 토큰은 더 이상 로그인 증명으로 사용할 수 없습니다.
        raise HTTPException(status_code=401, detail="토큰 사용 시간이 만료되었습니다.")
    except jwt.InvalidTokenError:
        # 서명이 다르거나 토큰 형식이 잘못된 경우입니다.
        raise HTTPException(status_code=401, detail="올바르지 않은 토큰입니다.")
