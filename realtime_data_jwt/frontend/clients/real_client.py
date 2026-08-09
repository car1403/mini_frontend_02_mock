import json

import httpx
import streamlit as st

from core.api_client import BACKEND_URL, BackendAPIError, request


def get_token() -> str:
    return st.session_state.get("access_token", "")


def create_real_data(data: dict):
    """백엔드가 Supabase 저장과 Redis 발행을 처리합니다."""

    return request(
        "POST",
        "/real-data",
        json=data,
        access_token=get_token(),
    )


def get_recent_real_data(limit: int = 20):
    """백엔드를 통해 Supabase 최근 데이터를 조회합니다."""

    return request(
        "GET",
        f"/real-data/recent?limit={limit}",
        access_token=get_token(),
    )


def receive_real_data():
    """Redis 이벤트를 전달하는 SSE에 연결합니다."""

    headers = {"Authorization": f"Bearer {get_token()}"}

    try:
        with httpx.stream(
            "GET",
            f"{BACKEND_URL}/real-data/stream",
            headers=headers,
            timeout=None,
        ) as response:
            if response.status_code == 401:
                raise BackendAPIError("로그인이 필요하거나 토큰이 만료되었습니다.")

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
