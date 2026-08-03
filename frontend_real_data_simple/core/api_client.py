import json
from typing import Any, Iterator

import httpx


BACKEND_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 15.0


class BackendAPIError(Exception):
    pass


def request(
    method: str,
    path: str,
    json: dict[str, Any] | None = None,
):
    try:
        response = httpx.request(
            method,
            f"{BACKEND_URL}{path}",
            json=json,
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.RequestError as error:
        raise BackendAPIError("백엔드 서버에 연결할 수 없습니다.") from error

    if response.is_error:
        try:
            detail = response.json().get("detail", "알 수 없는 오류")
        except ValueError:
            detail = response.text
        raise BackendAPIError(f"백엔드 요청 실패: {detail}")

    try:
        return response.json()
    except ValueError as error:
        raise BackendAPIError("백엔드가 올바른 JSON을 반환하지 않았습니다.") from error


def create_real_data(data: dict):
    """센서 데이터를 저장하고 실시간 이벤트로 발행합니다."""

    return request("POST", "/real-data", json=data)


def get_recent_real_data(limit: int = 20):
    """Supabase에 저장된 최근 센서 데이터를 조회합니다."""

    return request("GET", f"/real-data/recent?limit={limit}")


def receive_real_data() -> Iterator[tuple[str, dict]]:
    """SSE에 연결해 이벤트 이름과 데이터를 차례대로 반환합니다."""

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
                elif line.startswith("data: "):
                    data = json.loads(line.removeprefix("data: "))
                    yield event_name, data
                    event_name = ""
    except (httpx.HTTPError, json.JSONDecodeError) as error:
        raise BackendAPIError(f"실시간 연결에 실패했습니다: {error}") from error
