import asyncio
import json

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.schemes.real_scheme import RealData
from app.services.real_service import make_fake_data


real_router = APIRouter(prefix="/real", tags=["Real Data"])


@real_router.get("/one", response_model=RealData)
def get_one():
    """가상 온도 데이터 한 개를 바로 반환합니다."""

    return make_fake_data(1)


@real_router.get("/stream")
async def stream_data(
    count: int = Query(default=10, ge=1, le=30),
):
    """가상 온도를 1초 간격으로 SSE 전송합니다."""

    async def generate():
        for number in range(1, count + 1):
            fake_data = make_fake_data(number)
            json_text = json.dumps(fake_data, ensure_ascii=False)
            yield f"data: {json_text}\n\n"

            if number < count:
                await asyncio.sleep(1)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
