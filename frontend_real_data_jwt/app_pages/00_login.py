import streamlit as st

from core.auth import is_logged_in, login, logout


if not is_logged_in():
    st.title("로그인")
    st.caption("로그인하면 JWT가 발급되고 Product 메뉴를 사용할 수 있습니다.")

    with st.form("login_form"):
        login_id = st.text_input("아이디", value="id01")
        login_pwd = st.text_input("비밀번호", type="password", value="pwd01")
        submitted = st.form_submit_button("LOGIN")

    if submitted:
        login(login_id, login_pwd)
else:
    st.success("로그인되어 있습니다.")
    st.button("LOGOUT", on_click=logout)
