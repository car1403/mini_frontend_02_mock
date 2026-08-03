from typing import Any

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
