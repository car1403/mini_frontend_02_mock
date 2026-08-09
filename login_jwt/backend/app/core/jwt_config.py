import os


# 실제 서비스에서는 반드시 .env에 길고 복잡한 값을 넣어 사용합니다.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "beginner-jwt-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 30
