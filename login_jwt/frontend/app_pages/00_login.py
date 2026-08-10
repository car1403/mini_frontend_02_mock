"""아이디와 비밀번호를 입력받아 로그인하는 화면입니다."""

import streamlit as st

from core.auth import is_logged_in, login, logout


if not is_logged_in():
    st.title("로그인")
    st.caption("로그인하면 JWT가 발급되고 Product 메뉴를 사용할 수 있습니다.")

    # form을 사용하면 입력값을 LOGIN 버튼을 누를 때 한 번에 처리합니다.
    with st.form("login_form"):
        login_id = st.text_input("아이디", value="id01")
        login_pwd = st.text_input("비밀번호", type="password", value="pwd01")
        submitted = st.form_submit_button("LOGIN")

    if submitted:
        # login()이 백엔드에 로그인 요청을 보내고 JWT를 저장합니다.
        login(login_id, login_pwd)
else:
    # 이미 로그인한 사용자는 폼 대신 로그아웃 버튼을 봅니다.
    st.success("로그인되어 있습니다.")
    st.button("LOGOUT", on_click=logout)
