import json

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.core.auth_dependency import get_current_user
from app.schemes.real_scheme import RealData, RealDataCreate
from app.services.real_service import (
    get_recent_data,
    publish_real_data,
    save_real_data,
    subscribe_real_data,
)


real_router = APIRouter(tags=["Real Data"])


@real_router.post("/real-data", response_model=RealData)
async def create_real_data(
    data: RealDataCreate,
    current_user: str = Depends(get_current_user),
):
    """Supabase에 저장한 후 Redis로 실시간 이벤트를 발행합니다."""

    try:
        saved_item = save_real_data(data, current_user)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Supabase 저장에 실패했습니다. .env와 schema.sql을 확인해 주세요.",
        )

    try:
        await publish_real_data(saved_item)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail=(
                "Supabase 저장은 완료됐지만 Redis 발행에 실패했습니다. "
                "REDIS_URL을 확인해 주세요."
            ),
        )

    return saved_item


@real_router.get("/real-data/recent", response_model=list[RealData])
def recent_real_data(
    limit: int = Query(default=20, ge=1, le=100),
    current_user: str = Depends(get_current_user),
):
    """Supabase에 저장된 최근 데이터를 조회합니다."""

    try:
        return get_recent_data(limit)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Supabase 조회에 실패했습니다. .env와 schema.sql을 확인해 주세요.",
        )


@real_router.get("/real-data/stream")
async def stream_real_data(
    current_user: str = Depends(get_current_user),
):
    """Redis에 새로 발행된 데이터만 SSE로 전달합니다."""

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
