import json
from typing import Iterator

import httpx


BACKEND_URL = "http://127.0.0.1:8000"


class BackendAPIError(Exception):
    """사용자 화면이 백엔드와 통신할 때 발생하는 오류입니다."""

    pass


def receive_real_data() -> Iterator[tuple[str, dict]]:
    """SSE에 연결하고 실시간 이벤트를 하나씩 반환합니다."""

    try:
        with httpx.stream(
            "GET",
            f"{BACKEND_URL}/real-data/stream",
            # 실시간 응답은 계속 이어지므로 일반 요청처럼 제한 시간을 두지 않습니다.
            timeout=None,
        ) as response:
            response.raise_for_status()
            event_name = ""

            # SSE 응답은 여러 줄로 계속 도착하므로 한 줄씩 읽습니다.
            for line in response.iter_lines():
                # 예: event: real-data
                if line.startswith("event: "):
                    event_name = line.removeprefix("event: ")

                # 예: data: {"device_name": "sensor-01", ...}
                elif line.startswith("data: "):
                    json_text = line.removeprefix("data: ")
                    received_data = json.loads(json_text)
                    yield event_name, received_data
                    event_name = ""
    except (httpx.HTTPError, json.JSONDecodeError) as error:
        raise BackendAPIError(f"실시간 연결에 실패했습니다: {error}") from error
