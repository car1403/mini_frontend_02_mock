import json

import httpx


BACKEND_URL = "http://127.0.0.1:8000"


def receive_real_data(count: int = 10):
    """로그인 없이 SSE 데이터 한 줄씩을 JSON으로 바꿔 반환합니다."""

    try:
        with httpx.stream(
            "GET",
            f"{BACKEND_URL}/real/stream",
            params={"count": count},
            timeout=None,
        ) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if line.startswith("data: "):
                    json_text = line.removeprefix("data: ")
                    yield json.loads(json_text)
    except httpx.HTTPError as error:
        raise RuntimeError(
            "백엔드 실시간 서버에 연결할 수 없습니다."
        ) from error
