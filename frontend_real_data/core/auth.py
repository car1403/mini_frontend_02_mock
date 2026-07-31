"""로그인 상태와 JWT를 관리하는 공통 기능입니다."""

import streamlit as st

from clients.auth_client import login_process
from core.api_client import BackendAPIError


def init_state(
    stored_loginout: str = "logout",
    stored_login_id: str = "",
    stored_access_token: str = "",
) -> None:
    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", stored_login_id)
    st.session_state.setdefault("login_pwd", "")
    st.session_state.setdefault("access_token", stored_access_token)


def login(id: str, pwd: str) -> None:
    try:
        result = login_process(id, pwd)

        st.session_state.loginout = "login"
        st.session_state.login_id = id
        st.session_state.access_token = result["access_token"]
        st.rerun()
    except BackendAPIError as error:
        st.error(str(error))


def logout() -> None:
    # JWT 방식은 브라우저에 저장된 토큰을 지우면 로그아웃됩니다.
    st.session_state.loginout = "logout"
    st.session_state.login_id = ""
    st.session_state.login_pwd = ""
    st.session_state.access_token = ""


def is_logged_in() -> bool:
    return (
        st.session_state.get("loginout") == "login"
        and bool(st.session_state.get("access_token"))
    )
