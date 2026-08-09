import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_ROOT = Path(__file__).resolve().parents[2]
# load_dotenv()는 .env 파일에 적어 둔 값을 환경변수로 불러옵니다.
load_dotenv(BACKEND_ROOT / ".env")

# Supabase에 접속할 때 사용하는 주소와 관리자용 키입니다.
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

# Redis URL은 REST 주소가 아니라 rediss://로 시작하는 TCP/TLS 주소입니다.
REDIS_URL = os.getenv("REDIS_URL", "").strip()

# Redis Key가 아니라 실시간 메시지를 주고받는 Pub/Sub 채널 이름입니다.
REDIS_CHANNEL = "beginner:real-data"


def check_supabase_config() -> None:
    """Supabase 접속에 필요한 두 설정값이 있는지 확인합니다."""

    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY를 설정해 주세요.")


def check_redis_config() -> None:
    """Redis 접속 주소가 설정되어 있는지 확인합니다."""

    if not REDIS_URL:
        raise RuntimeError("Upstash의 REDIS_URL을 설정해 주세요.")
