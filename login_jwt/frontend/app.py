"""로그인 상태에 따라 Streamlit 메뉴를 구성하는 프론트엔드 시작 파일입니다."""

import streamlit as st
from streamlit_session_browser_storage import SessionStorage

from core.auth import init_state, logout


st.set_page_config(page_title="JWT Login", page_icon="🔐", layout="wide")

# SessionStorage는 새로고침 후에도 같은 브라우저 탭에 로그인 정보를 유지합니다.
storage = SessionStorage(key="jwt_login_session_storage")

# 브라우저 저장소에 값이 없으면 로그아웃 상태와 빈 문자열을 기본값으로 사용합니다.
stored_loginout = storage.getItem("loginout") or "logout"
stored_login_id = storage.getItem("login_id") or ""
stored_access_token = storage.getItem("access_token") or ""

if "loginout" not in st.session_state:
    # Streamlit 세션이 처음 만들어질 때 브라우저에 저장했던 값을 복원합니다.
    init_state(stored_loginout, stored_login_id, stored_access_token)

if st.session_state.loginout == "logout":
    # 로그아웃 상태라면 브라우저에 남아 있는 로그인 정보도 모두 삭제합니다.
    storage.deleteAll(key="jwt_login_session_storage")
else:
    # 로그인 상태와 JWT를 브라우저 저장소에 기록하여 새로고침에도 유지합니다.
    storage.setItem("loginout", "login", key="save_loginout")
    storage.setItem("login_id", st.session_state.login_id, key="save_login_id")
    storage.setItem(
        "access_token",
        st.session_state.access_token,
        key="save_access_token",
    )

# 각 Python 화면 파일을 Streamlit 페이지 객체로 등록합니다.
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
    # 로그인한 사용자에게는 JWT가 필요한 상품 화면을 보여 줍니다.
    pages = [home_page, weather_page, product_select_page, product_create_page]
else:
    # 로그인 전에는 로그인·회원가입·서버 확인 화면만 보여 줍니다.
    pages = [home_page, login_page, signup_page, health_page]

navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    # 사이드바 메뉴도 현재 로그인 상태에 맞춰 다르게 구성합니다.
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

# 선택된 페이지 파일의 코드를 실행하여 화면에 표시합니다.
navigation.run()
