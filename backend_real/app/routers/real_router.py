import asyncio
import json

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from app.core.auth_dependency import get_current_user
from app.schemes.real_scheme import RealData
from app.services.real_service import make_fake_data


real_router = APIRouter(tags=["Real Data"])


@real_router.get("/real/one")
def get_one(
    current_user: str = Depends(get_current_user),
) -> RealData:
    """가상 데이터를 한 개 반환합니다."""

    return make_fake_data(1)


@real_router.get("/real/stream")
async def stream_data(
    count: int = Query(default=10, ge=1, le=30),
    current_user: str = Depends(get_current_user),
) -> StreamingResponse:
    """1초마다 가상 데이터를 하나씩 SSE 형식으로 반환합니다."""

    async def generate():
        for number in range(1, count + 1):
            fake_data = make_fake_data(number)
            json_text = json.dumps(fake_data, ensure_ascii=False)

            # SSE는 각 데이터를 "data: 내용 + 빈 줄" 형태로 보냅니다.
            yield f"data: {json_text}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
