import streamlit as st

from clients.auth_client import login_process
from core.api_client import BackendAPIError


def init_state(
    stored_loginout: str = "logout",
    stored_login_id: str = "",
    stored_login_email: str = "",
    stored_login_name: str = "",
    stored_user_role: str = "",
    stored_access_token: str = "",
) -> None:
    """브라우저에 저장했던 로그인 정보와 역할을 Streamlit 세션에 복원합니다."""

    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", stored_login_id)
    st.session_state.setdefault("login_email", stored_login_email)
    st.session_state.setdefault("login_name", stored_login_name)
    st.session_state.setdefault("user_role", stored_user_role)
    st.session_state.setdefault("access_token", stored_access_token)


def login(email: str, pwd: str) -> None:
    """Supabase Auth 로그인 결과의 사용자 정보, 역할, Access Token을 저장합니다."""

    try:
        result = login_process(email, pwd)
        user = result["user"]

        st.session_state.loginout = "login"
        st.session_state.login_id = user["id"]
        st.session_state.login_email = user["email"]
        st.session_state.login_name = user["name"]
        st.session_state.user_role = user["role"]
        st.session_state.access_token = result["access_token"]
        st.rerun()
    except BackendAPIError as error:
        st.error(str(error))


def logout() -> None:
    st.session_state.loginout = "logout"
    st.session_state.login_id = ""
    st.session_state.login_email = ""
    st.session_state.login_name = ""
    st.session_state.user_role = ""
    st.session_state.access_token = ""


def is_logged_in() -> bool:
    return (
        st.session_state.get("loginout") == "login"
        and bool(st.session_state.get("access_token"))
    )


def is_admin() -> bool:
    """로그인 응답에서 받은 역할이 admin인지 확인합니다."""

    return is_logged_in() and st.session_state.get("user_role") == "admin"
