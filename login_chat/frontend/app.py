import streamlit as st
from streamlit_session_browser_storage import SessionStorage

from core.auth import init_state, is_logged_in, logout


st.set_page_config(
    page_title="Login Chat",
    page_icon="💬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 980px; padding-top: 2rem; }
    [data-testid="stSidebar"] { background: #f7f9fc; }
    [data-testid="stChatMessage"] {
        border: 1px solid #e7ebf0;
        border-radius: 16px;
        padding: 0.4rem 0.8rem;
        margin-bottom: 0.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

storage = SessionStorage(key="login_chat_session")

stored_loginout = storage.getItem("loginout") or "logout"
stored_login_id = storage.getItem("login_id") or ""
stored_login_name = storage.getItem("login_name") or ""
stored_session_token = storage.getItem("session_token") or ""

if "loginout" not in st.session_state:
    init_state(
        stored_loginout,
        stored_login_id,
        stored_login_name,
        stored_session_token,
    )

if is_logged_in():
    storage.setItem("loginout", "login", key="save_loginout")
    storage.setItem("login_id", st.session_state.login_id, key="save_login_id")
    storage.setItem(
        "login_name",
        st.session_state.login_name,
        key="save_login_name",
    )
    storage.setItem(
        "session_token",
        st.session_state.session_token,
        key="save_session_token",
    )
else:
    storage.deleteAll(key="login_chat_session")

home_page = st.Page("app_pages/01_home.py", title="홈", icon="🏠", default=True)
login_page = st.Page("app_pages/00_login.py", title="로그인", icon="🔐")
chat_page = st.Page("app_pages/05_chat.py", title="AI Chat", icon="💬")

pages = [home_page, chat_page] if is_logged_in() else [home_page, login_page]
navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    st.title("💬 Login Chat")
    st.caption("로그인한 사용자만 이용할 수 있습니다.")
    st.divider()
    st.page_link(home_page, use_container_width=True)

    if is_logged_in():
        st.page_link(chat_page, use_container_width=True)
        st.divider()
        st.success(f"{st.session_state.login_name}님")
        st.caption(f"ID: {st.session_state.login_id}")
        st.button("로그아웃", on_click=logout, use_container_width=True)
    else:
        st.page_link(login_page, use_container_width=True)

navigation.run()
