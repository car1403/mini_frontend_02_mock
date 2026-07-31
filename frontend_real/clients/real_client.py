import json

import httpx
import streamlit as st

from core.api_client import BACKEND_URL, BackendAPIError


def receive_real_data(count: int):
    """백엔드 SSE에 연결하고 데이터를 하나씩 반환합니다."""

    token = st.session_state.get("access_token", "")
    headers = {"Authorization": f"Bearer {token}"}

    try:
        with httpx.stream(
            "GET",
            f"{BACKEND_URL}/real/stream",
            params={"count": count},
            headers=headers,
            timeout=None,
        ) as response:
            if response.status_code == 401:
                raise BackendAPIError("로그인이 필요하거나 토큰이 만료되었습니다.")

            response.raise_for_status()

            for line in response.iter_lines():
                if line.startswith("data: "):
                    json_text = line.removeprefix("data: ")
                    yield json.loads(json_text)
    except httpx.HTTPError as error:
        raise BackendAPIError(f"실시간 연결에 실패했습니다: {error}") from error
