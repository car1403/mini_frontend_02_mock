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
    """백엔드에 HTTP 요청을 보내고 JSON 응답을 반환합니다."""

    # 요청마다 필요한 HTTP 헤더를 담을 빈 딕셔너리를 만듭니다.
    headers = {}

    if access_token:
        # 보호된 API는 "Bearer JWT문자열" 형식의 Authorization 헤더가 필요합니다.
        headers["Authorization"] = f"Bearer {access_token}"

    try:
        # method와 path를 인자로 받아 GET, POST, PUT, DELETE 요청을 공통 처리합니다.
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
        # 401은 JWT가 없거나, 잘못됐거나, 만료된 경우입니다.
        raise BackendAPIError("로그인이 필요하거나 토큰이 만료되었습니다.")

    if response.is_error:
        # 그 밖의 4xx와 5xx 상태 코드도 프론트엔드용 오류로 바꿉니다.
        raise BackendAPIError(f"백엔드 요청 실패: {response.status_code}")

    try:
        # 정상 응답의 JSON 문자열을 Python 딕셔너리나 리스트로 변환합니다.
        return response.json()
    except ValueError as error:
        raise BackendAPIError("백엔드가 올바른 JSON을 반환하지 않았습니다.") from error
