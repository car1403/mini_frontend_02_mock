import streamlit as st

from clients.auth_client import signup_process
from core.api_client import BackendAPIError


st.title("회원가입")
st.caption("Supabase Auth에 가입하며 처음 역할은 일반 사용자(user)입니다.")

with st.form("signup_form", clear_on_submit=True):
    signup_email = st.text_input("이메일", placeholder="user@example.com")
    signup_pwd = st.text_input(
        "비밀번호",
        type="password",
        placeholder="4글자 이상",
    )
    signup_pwd_confirm = st.text_input("비밀번호 확인", type="password")
    signup_name = st.text_input("이름")
    submitted = st.form_submit_button(
        "회원가입",
        type="primary",
        use_container_width=True,
    )

if submitted:
    if signup_pwd != signup_pwd_confirm:
        st.warning("비밀번호와 비밀번호 확인이 다릅니다.")
    else:
        try:
            result = signup_process(
                signup_email.strip(),
                signup_pwd,
                signup_name.strip(),
            )
            st.success(f"{result['name']}님, 회원가입이 완료되었습니다.")
            st.info("왼쪽의 로그인 메뉴에서 새 계정으로 로그인하세요.")
        except BackendAPIError as error:
            st.error(str(error))
