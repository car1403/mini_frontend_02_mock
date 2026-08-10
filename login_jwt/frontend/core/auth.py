"""로그인 상태와 JWT를 관리하는 공통 기능입니다."""

import streamlit as st

from clients.auth_client import login_process
from core.api_client import BackendAPIError


def init_state(
    stored_loginout: str = "logout",
    stored_login_id: str = "",
    stored_access_token: str = "",
) -> None:
    """Streamlit 로그인 상태를 최초 한 번만 기본값으로 초기화합니다."""

    # setdefault는 키가 이미 있으면 기존 값을 유지하고, 없을 때만 값을 넣습니다.
    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", stored_login_id)
    st.session_state.setdefault("login_pwd", "")
    st.session_state.setdefault("access_token", stored_access_token)


def login(id: str, pwd: str) -> None:
    """백엔드 로그인을 요청하고 성공하면 사용자 ID와 JWT를 저장합니다."""

    try:
        result = login_process(id, pwd)

        # session_state 값은 Streamlit이 화면을 다시 실행해도 같은 세션에서 유지됩니다.
        st.session_state.loginout = "login"
        st.session_state.login_id = id
        st.session_state.access_token = result["access_token"]
        # 변경된 로그인 상태에 맞는 메뉴를 즉시 표시하도록 앱을 다시 실행합니다.
        st.rerun()
    except BackendAPIError as error:
        st.error(str(error))


def logout() -> None:
    """프론트엔드에 저장된 로그인 정보와 JWT를 모두 비웁니다."""

    # JWT 방식은 브라우저에 저장된 토큰을 지우면 로그아웃됩니다.
    st.session_state.loginout = "logout"
    st.session_state.login_id = ""
    st.session_state.login_pwd = ""
    st.session_state.access_token = ""


def is_logged_in() -> bool:
    """로그인 상태이고 JWT도 저장되어 있을 때만 True를 반환합니다."""

    return (
        st.session_state.get("loginout") == "login"
        and bool(st.session_state.get("access_token"))
    )
