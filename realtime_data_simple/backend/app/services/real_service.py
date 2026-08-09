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
    """설정값을 확인한 후 Supabase 연결 객체를 만듭니다."""

    check_supabase_config()
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def save_real_data(data: RealDataCreate) -> dict:
    """센서 데이터를 Supabase에 저장하고 저장된 데이터를 반환합니다."""

    # Pydantic 모델을 Supabase에 넣을 수 있는 딕셔너리로 바꿉니다.
    sensor_data = data.model_dump()

    # realtime_sensor_data 테이블에 한 행을 추가합니다.
    response = (
        get_supabase()
        .table("realtime_sensor_data")
        .insert(sensor_data)
        .execute()
    )

    if not response.data:
        raise RuntimeError("Supabase 저장 결과가 없습니다.")

    # insert 결과는 목록이므로 첫 번째 저장 데이터를 반환합니다.
    return response.data[0]


def get_recent_data(limit: int) -> list[dict]:
    """Supabase에서 최근 데이터를 조회합니다."""

    response = (
        get_supabase()
        .table("realtime_sensor_data")
        .select("*")
        # created_at을 내림차순으로 정렬하면 최신 데이터가 먼저 나옵니다.
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []


async def publish_real_data(saved_data: dict) -> None:
    """저장된 센서 데이터를 Redis 채널로 실시간 전송합니다."""

    check_redis_config()

    import redis.asyncio as redis

    # decode_responses=True를 사용하면 Redis 응답을 문자열로 받습니다.
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    message = json.dumps(saved_data, ensure_ascii=False)

    try:
        # 지정된 채널을 구독 중인 모든 클라이언트에게 메시지를 보냅니다.
        await redis_client.publish(REDIS_CHANNEL, message)
    finally:
        # 성공하거나 오류가 발생해도 Redis 연결은 항상 닫습니다.
        await redis_client.aclose()


async def subscribe_real_data():
    """Redis 채널을 계속 지켜보다가 새 데이터를 하나씩 반환합니다."""

    check_redis_config()

    import redis.asyncio as redis

    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_pubsub = redis_client.pubsub()

    # publish_real_data()가 사용하는 채널과 같은 채널을 구독합니다.
    await redis_pubsub.subscribe(REDIS_CHANNEL)

    try:
        while True:
            # 새 메시지를 최대 1초 동안 기다립니다.
            message = await redis_pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1,
            )

            if message and message.get("data"):
                # Redis에서 받은 JSON 문자열을 다시 딕셔너리로 바꿉니다.
                # yield는 값을 하나 반환하는 것처럼 라우터의 received_data에 전달합니다.
                # return은 값을 반환한 뒤 함수가 끝나지만, yield는 함수를 끝내지 않고 잠시 멈춥니다.
                # 다음 실행에서는 멈춘 위치부터 이어서 다음 Redis 메시지를 기다립니다.
                yield json.loads(message["data"])

            # 반복문이 CPU를 지나치게 사용하지 않도록 아주 잠깐 기다립니다.
            await asyncio.sleep(0.1)
    finally:
        # 스트림이 끝나면 구독과 Redis 연결을 순서대로 닫습니다.
        await redis_pubsub.unsubscribe(REDIS_CHANNEL)
        await redis_pubsub.aclose()
        await redis_client.aclose()
