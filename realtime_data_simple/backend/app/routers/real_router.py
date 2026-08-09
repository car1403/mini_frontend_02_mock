import json

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


@real_router.post("", response_model=RealDataResult)
async def create_real_data(data: RealDataCreate):
    """센서 데이터를 저장한 후 Redis로 실시간 전송합니다."""

    # 1. 프론트엔드에서 받은 센서 데이터를 Supabase에 저장합니다.
    try:
        saved_data = save_real_data(data)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="센서 데이터 저장에 실패했습니다.",
        ) from error

    # 2. 저장된 데이터를 Redis 채널로 전송합니다.
    try:
        await publish_real_data(saved_data)
        saved_data["event_published"] = True
    except Exception:
        # Redis 전송에 실패해도 Supabase 저장은 이미 성공한 상태입니다.
        # 사용자가 같은 데이터를 다시 입력해 중복 저장하지 않도록 정상 응답을 반환합니다.
        saved_data["event_published"] = False

    # 3. 저장된 데이터와 Redis 전송 결과를 프론트엔드에 반환합니다.
    return saved_data


@real_router.get("/recent", response_model=list[RealData])
def recent_real_data(limit: int = Query(default=20, ge=1, le=100)):
    """Supabase에 저장된 최근 센서 데이터를 조회합니다."""

    try:
        return get_recent_data(limit)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="최근 센서 데이터 조회에 실패했습니다.",
        ) from error


@real_router.get("/stream")
async def stream_real_data():
    """Redis에서 받은 데이터를 SSE 형식으로 프론트엔드에 전달합니다."""

    async def generate():
        """SSE 규칙에 맞는 문자열을 하나씩 만들어 반환합니다."""

        try:
            async for received_data in subscribe_real_data():
                # SSE는 event와 data를 문자열로 보내며 빈 줄로 이벤트를 구분합니다.
                json_text = json.dumps(received_data, ensure_ascii=False)

                # yield는 SSE 이벤트 하나를 사용자 브라우저로 전송합니다.
                # return과 달리 함수가 끝나지 않으므로 다음 센서 데이터도 계속 전송할 수 있습니다.
                yield f"event: real-data\ndata: {json_text}\n\n"
        except Exception:
            # Redis 연결 오류도 SSE 이벤트로 보내 프론트엔드가 표시할 수 있게 합니다.
            error_text = json.dumps(
                {"error": "Redis 실시간 연결에 실패했습니다."},
                ensure_ascii=False,
            )
            yield f"event: error\ndata: {error_text}\n\n"

    return StreamingResponse(
        generate(),
        # 브라우저에 이 응답이 SSE 스트림임을 알려 주는 Content-Type입니다.
        media_type="text/event-stream",
        headers={
            # 중간 서버가 실시간 데이터를 저장하거나 모아서 보내지 않도록 설정합니다.
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
