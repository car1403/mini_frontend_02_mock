import streamlit as st

from clients.auth_client import login_process, logout_process
from core.api_client import BackendAPIError


def init_state(
    stored_loginout: str = "logout",
    stored_login_id: str = "",
    stored_login_name: str = "",
    stored_session_token: str = "",
) -> None:
    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", stored_login_id)
    st.session_state.setdefault("login_name", stored_login_name)
    st.session_state.setdefault("session_token", stored_session_token)
    st.session_state.setdefault("chat_messages", [])


def login(id: str, pwd: str) -> None:
    try:
        result = login_process(id, pwd)
        user = result["user"]

        st.session_state.loginout = "login"
        st.session_state.login_id = user["id"]
        st.session_state.login_name = user["name"]
        st.session_state.session_token = result["session_token"]
        st.session_state.chat_messages = []
        st.rerun()
    except BackendAPIError as error:
        st.error(str(error))


def logout() -> None:
    token = st.session_state.get("session_token", "")

    if token:
        try:
            logout_process(token)
        except BackendAPIError:
            pass

    st.session_state.loginout = "logout"
    st.session_state.login_id = ""
    st.session_state.login_name = ""
    st.session_state.session_token = ""
    st.session_state.chat_messages = []


def is_logged_in() -> bool:
    return (
        st.session_state.get("loginout") == "login"
        and bool(st.session_state.get("session_token"))
    )
