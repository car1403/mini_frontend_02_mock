import streamlit as st

from clients.auth_client import login_process
from core.api_client import BackendAPIError


def init_state(
    stored_loginout: str = "logout",
    stored_login_id: str = "",
    stored_login_name: str = "",
    stored_access_token: str = "",
) -> None:
    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", stored_login_id)
    st.session_state.setdefault("login_name", stored_login_name)
    st.session_state.setdefault("access_token", stored_access_token)


def login(id: str, pwd: str) -> None:
    try:
        result = login_process(id, pwd)
        user = result["user"]

        st.session_state.loginout = "login"
        st.session_state.login_id = user["id"]
        st.session_state.login_name = user["name"]
        st.session_state.access_token = result["access_token"]
        st.rerun()
    except BackendAPIError as error:
        st.error(str(error))


def logout() -> None:
    st.session_state.loginout = "logout"
    st.session_state.login_id = ""
    st.session_state.login_name = ""
    st.session_state.access_token = ""


def is_logged_in() -> bool:
    return (
        st.session_state.get("loginout") == "login"
        and bool(st.session_state.get("access_token"))
    )
