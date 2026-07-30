"""공통 로그인 상태와 인증 동작을 관리합니다."""

import streamlit as st
from clients.auth_client import login_process, logout_process
from core.api_client import BackendAPIError

def init_state(stored_loginout: str = "logout") -> None:
    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", "")
    st.session_state.setdefault("login_pwd", "")
    st.session_state.setdefault("login_name", "")


def login(id:str, pwd:str) -> None:
    try:
        result = login_process(id, pwd)
        if result is not None:
            st.session_state.loginout = "login"
            st.session_state.login_id = id
            st.session_state.login_name = result["name"]
            st.rerun()
    except BackendAPIError as error:
            st.error(str(error))    


def logout() -> None:
    result = logout_process(st.session_state.login_id)
    if result is not None:
        st.session_state.loginout = "logout"
        st.session_state.login_id = ""
        st.session_state.login_pwd = ""
        st.session_state.login_name = ""


def is_logged_in() -> bool:
    return st.session_state.loginout == "login"
