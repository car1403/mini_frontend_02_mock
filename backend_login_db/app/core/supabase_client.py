import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL", "").strip()
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not url or not service_key:
        raise RuntimeError("SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY를 설정해 주세요.")
    return create_client(url, service_key)
