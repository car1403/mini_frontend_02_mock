import streamlit as st

from core.auth import is_logged_in, login


st.title("🔐 로그인")
st.caption("로그인하면 AI Chat 메뉴가 열립니다.")

if is_logged_in():
    st.success("이미 로그인되어 있습니다.")
else:
    left, center, right = st.columns([1, 1.4, 1])

    with center:
        with st.container(border=True):
            st.subheader("Welcome back")
            st.write("학습용 계정으로 로그인해 주세요.")

            with st.form("login_form"):
                login_id = st.text_input("아이디", value="id01")
                login_pwd = st.text_input(
                    "비밀번호",
                    type="password",
                    value="pwd01",
                )
                submitted = st.form_submit_button(
                    "로그인",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                login(login_id, login_pwd)

            st.caption("테스트 계정: id01 / pwd01")
