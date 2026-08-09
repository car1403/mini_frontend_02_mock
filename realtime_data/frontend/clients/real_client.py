import json

import httpx

from core.api_client import BACKEND_URL, BackendAPIError, request


def create_real_data(data: dict):
    return request("POST", "/real-data", json=data)


def get_recent_real_data(limit: int = 20):
    return request("GET", f"/real-data/recent?limit={limit}")


def receive_real_data():
    """로그인 없이 Redis 이벤트를 전달하는 SSE에 연결합니다."""

    try:
        with httpx.stream(
            "GET",
            f"{BACKEND_URL}/real-data/stream",
            timeout=None,
        ) as response:
            response.raise_for_status()
            event_name = ""

            for line in response.iter_lines():
                if line.startswith("event: "):
                    event_name = line.removeprefix("event: ")

                if line.startswith("data: "):
                    data = json.loads(line.removeprefix("data: "))
                    yield event_name, data
                    event_name = ""
    except httpx.HTTPError as error:
        raise BackendAPIError(f"실시간 연결에 실패했습니다: {error}") from error
