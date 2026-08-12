import streamlit as st

from core.auth import is_logged_in, login, logout


if not is_logged_in():
    st.title("로그인")
    st.caption("Supabase Auth로 로그인하면 역할에 맞는 Product 메뉴가 표시됩니다.")

    with st.form("login_form"):
        login_email = st.text_input("이메일")
        login_pwd = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("LOGIN")

    if submitted:
        login(login_email.strip(), login_pwd)
else:
    st.success("로그인되어 있습니다.")
    st.button("LOGOUT", on_click=logout)
