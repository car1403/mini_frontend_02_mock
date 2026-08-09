import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

# Upstash의 Redis Protocol 주소입니다. rediss:// 로 시작해야 합니다.
REDIS_URL = os.getenv("REDIS_URL", "").strip()
REDIS_CHANNEL = "beginner:real-data"


def check_supabase_config() -> None:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY를 설정해 주세요.")


def check_redis_config() -> None:
    if not REDIS_URL:
        raise RuntimeError("Upstash의 REDIS_URL을 설정해 주세요.")
