import streamlit as st
from streamlit_session_browser_storage import SessionStorage

from core.auth import init_state, logout


st.set_page_config(page_title="JWT Login", page_icon="🔐", layout="wide")

storage = SessionStorage(key="jwt_login_session_storage")

stored_loginout = storage.getItem("loginout") or "logout"
stored_login_id = storage.getItem("login_id") or ""
stored_access_token = storage.getItem("access_token") or ""

if "loginout" not in st.session_state:
    init_state(stored_loginout, stored_login_id, stored_access_token)

if st.session_state.loginout == "logout":
    storage.deleteAll(key="jwt_login_session_storage")
else:
    storage.setItem("loginout", "login", key="save_loginout")
    storage.setItem("login_id", st.session_state.login_id, key="save_login_id")
    storage.setItem(
        "access_token",
        st.session_state.access_token,
        key="save_access_token",
    )

home_page = st.Page("app_pages/01_home.py", title="홈", icon="🏠", default=True)
login_page = st.Page("app_pages/00_login.py", title="로그인", icon="🔐")
signup_page = st.Page("app_pages/02_signup.py", title="회원가입", icon="📝")
weather_page = st.Page("app_pages/03_weather.py", title="날씨조회", icon="🌤️")
health_page = st.Page("app_pages/04_health.py", title="서버체크", icon="🩺")
product_select_page = st.Page(
    "app_pages/product_select.py",
    title="Product 조회",
    icon="📋",
)
product_create_page = st.Page(
    "app_pages/product_create.py",
    title="Product 입력",
    icon="➕",
)

if st.session_state.loginout == "login" and st.session_state.access_token:
    pages = [home_page, weather_page, product_select_page, product_create_page]
else:
    pages = [home_page, login_page, signup_page, health_page]

navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    st.page_link(home_page)

    if st.session_state.loginout == "login" and st.session_state.access_token:
        st.button("LOGOUT", on_click=logout, use_container_width=True)
        st.page_link(weather_page)
        st.page_link(product_select_page)
        st.page_link(product_create_page)
    else:
        st.page_link(login_page)
        st.page_link(signup_page)
        st.page_link(health_page)

navigation.run()
