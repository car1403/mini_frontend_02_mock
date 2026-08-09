import asyncio
import json

from supabase import Client, create_client

from app.core.real_config import (
    REDIS_CHANNEL,
    REDIS_URL,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_URL,
    check_redis_config,
    check_supabase_config,
)
from app.schemes.real_scheme import RealDataCreate


def get_supabase() -> Client:
    check_supabase_config()
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def save_real_data(data: RealDataCreate, user_id: str) -> dict:
    """센서 데이터를 Supabase에 영구 저장합니다."""

    payload = data.model_dump()
    payload["created_by"] = user_id

    result = get_supabase().table("realtime_sensor_data_jwt").insert(payload).execute()

    if not result.data:
        raise RuntimeError("Supabase 저장 결과가 없습니다.")

    return result.data[0]


def get_recent_data(limit: int) -> list[dict]:
    """Supabase에서 최근 데이터를 조회합니다."""

    result = (
        get_supabase()
        .table("realtime_sensor_data_jwt")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []


async def publish_real_data(item: dict) -> None:
    """저장된 데이터를 Upstash Redis 채널로 발행합니다."""

    check_redis_config()

    import redis.asyncio as redis

    client = redis.from_url(REDIS_URL, decode_responses=True)
    try:
        await client.publish(
            REDIS_CHANNEL,
            json.dumps(item, ensure_ascii=False),
        )
    finally:
        await client.aclose()


async def subscribe_real_data():
    """Upstash Redis 채널을 구독하고 새 데이터를 하나씩 반환합니다."""

    check_redis_config()

    import redis.asyncio as redis

    client = redis.from_url(REDIS_URL, decode_responses=True)
    pubsub = client.pubsub()
    await pubsub.subscribe(REDIS_CHANNEL)
    seconds_without_data = 0

    try:
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1,
            )

            if message and message.get("data"):
                seconds_without_data = 0
                yield json.loads(message["data"])
            else:
                seconds_without_data += 1

            # 데이터가 없을 때도 연결이 살아 있음을 5초마다 알려 줍니다.
            if seconds_without_data >= 5:
                yield {"_event": "heartbeat"}
                seconds_without_data = 0

            await asyncio.sleep(0.1)
    finally:
        await pubsub.unsubscribe(REDIS_CHANNEL)
        await pubsub.aclose()
        await client.aclose()
