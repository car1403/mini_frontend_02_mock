"""백엔드에 HTTP 요청을 보내는 공통 기능입니다."""

from typing import Any

import httpx


BACKEND_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 15.0


class BackendAPIError(Exception):
    """백엔드 연결 또는 API 응답 처리 중 발생한 오류입니다."""


def request(
    method: str,
    path: str,
    json: dict[str, Any] | None = None,
    access_token: str | None = None,
):
    headers = {}

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    try:
        response = httpx.request(
            method,
            f"{BACKEND_URL}{path}",
            json=json,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.TimeoutException as error:
        raise BackendAPIError("백엔드 응답 시간이 초과되었습니다.") from error
    except httpx.RequestError as error:
        raise BackendAPIError(
            "백엔드 서버에 연결할 수 없습니다. 서버 실행 상태를 확인해 주세요."
        ) from error

    if response.status_code == 401:
        raise BackendAPIError("로그인이 필요하거나 토큰이 만료되었습니다.")

    if response.is_error:
        raise BackendAPIError(f"백엔드 요청 실패: {response.status_code}")

    try:
        return response.json()
    except ValueError as error:
        raise BackendAPIError("백엔드가 올바른 JSON을 반환하지 않았습니다.") from error
