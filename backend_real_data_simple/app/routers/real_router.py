import json
import logging

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.schemes.real_scheme import RealData, RealDataCreate, RealDataResult
from app.services.real_service import (
    get_recent_data,
    publish_real_data,
    save_real_data,
    subscribe_real_data,
)


real_router = APIRouter(prefix="/real-data", tags=["Real Data"])
logger = logging.getLogger(__name__)


@real_router.post("", response_model=RealDataResult)
async def create_real_data(data: RealDataCreate):
    """Supabase에 저장한 후 Redis로 실시간 이벤트를 발행합니다."""

    try:
        saved_item = save_real_data(data)
    except Exception as error:
        logger.exception("Supabase 저장 실패")
        raise HTTPException(
            status_code=503,
            detail="Supabase 저장에 실패했습니다. .env와 schema.sql을 확인해 주세요.",
        ) from error

    try:
        await publish_real_data(saved_item)
        saved_item["event_published"] = True
    except Exception:
        # 저장은 이미 완료됐으므로 실패 응답을 보내 재입력과 중복 저장을 유도하지 않습니다.
        logger.exception("Redis 발행 실패")
        saved_item["event_published"] = False

    return saved_item


@real_router.get("/recent", response_model=list[RealData])
def recent_real_data(limit: int = Query(default=20, ge=1, le=100)):
    """Supabase에 저장된 최근 데이터를 조회합니다."""

    try:
        return get_recent_data(limit)
    except Exception as error:
        logger.exception("Supabase 조회 실패")
        raise HTTPException(
            status_code=503,
            detail="Supabase 조회에 실패했습니다. .env와 schema.sql을 확인해 주세요.",
        ) from error


@real_router.get("/stream")
async def stream_real_data():
    """Redis에 새로 발행된 데이터를 SSE로 전달합니다."""

    async def generate():
        try:
            async for item in subscribe_real_data():
                event_name = item.pop("_event", "real-data")
                json_text = json.dumps(item, ensure_ascii=False)
                yield f"event: {event_name}\ndata: {json_text}\n\n"
        except Exception:
            error_text = json.dumps(
                {"error": "Redis 연결에 실패했습니다. REDIS_URL을 확인해 주세요."},
                ensure_ascii=False,
            )
            yield f"event: error\ndata: {error_text}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
