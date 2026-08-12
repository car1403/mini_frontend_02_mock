import streamlit as st
from streamlit_session_browser_storage import SessionStorage

from core.auth import init_state, logout


st.set_page_config(page_title="Product RLS", page_icon="🔐", layout="wide")

storage = SessionStorage(key="jwt_rls_product_session_storage")

stored_loginout = storage.getItem("loginout") or "logout"
stored_login_id = storage.getItem("login_id") or ""
stored_login_email = storage.getItem("login_email") or ""
stored_login_name = storage.getItem("login_name") or ""
stored_user_role = storage.getItem("user_role") or ""
stored_access_token = storage.getItem("access_token") or ""

if "loginout" not in st.session_state:
    init_state(
        stored_loginout,
        stored_login_id,
        stored_login_email,
        stored_login_name,
        stored_user_role,
        stored_access_token,
    )

if st.session_state.loginout == "logout":
    storage.deleteAll(key="jwt_rls_product_session_storage")
else:
    storage.setItem("loginout", "login", key="save_loginout")
    storage.setItem("login_id", st.session_state.login_id, key="save_login_id")
    storage.setItem("login_email", st.session_state.login_email, key="save_login_email")
    storage.setItem("login_name", st.session_state.login_name, key="save_login_name")
    storage.setItem("user_role", st.session_state.user_role, key="save_user_role")
    storage.setItem("access_token", st.session_state.access_token, key="save_access_token")

home_page = st.Page("app_pages/01_home.py", title="홈", icon="🏠", default=True)
login_page = st.Page("app_pages/00_login.py", title="로그인", icon="🔐")
signup_page = st.Page("app_pages/02_signup.py", title="회원가입", icon="📝")
health_page = st.Page("app_pages/04_health.py", title="서버체크", icon="🩺")
product_select_page = st.Page(
    "app_pages/product_select.py", title="Product 조회", icon="📋"
)
product_create_page = st.Page(
    "app_pages/product_create.py", title="Product 입력", icon="➕"
)

if st.session_state.loginout == "login" and st.session_state.access_token:
    # 일반 사용자는 조회만, 관리자는 조회와 입력 메뉴를 모두 볼 수 있습니다.
    pages = [home_page, product_select_page]
    if st.session_state.user_role == "admin":
        pages.append(product_create_page)
else:
    pages = [home_page, login_page, signup_page, health_page]

navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    st.page_link(home_page)

    if st.session_state.loginout == "login" and st.session_state.access_token:
        st.write(f"역할: **{st.session_state.user_role}**")
        st.button("LOGOUT", on_click=logout, use_container_width=True)
        st.page_link(product_select_page)

        if st.session_state.user_role == "admin":
            st.page_link(product_create_page)
    else:
        st.page_link(login_page)
        st.page_link(signup_page)
        st.page_link(health_page)

navigation.run()
