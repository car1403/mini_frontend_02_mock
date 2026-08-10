"""JWT를 만들고 검증할 때 함께 사용하는 설정값입니다."""

import os


# 실제 서비스에서는 반드시 .env에 길고 복잡한 값을 넣어 사용합니다.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "beginner-jwt-secret-key")
# 로그인할 때 토큰 생성과 API 요청 때 토큰 검증에서 같은 알고리즘을 사용해야 합니다.
JWT_ALGORITHM = "HS256"
# 발급된 JWT는 30분 동안 사용할 수 있습니다.
JWT_EXPIRE_MINUTES = 30
