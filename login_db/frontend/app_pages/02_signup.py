import streamlit as st

from clients.auth_client import signup_process
from core.api_client import BackendAPIError


st.title("회원가입")
st.caption("회원 정보는 backend를 통해 Supabase customers 테이블에 저장됩니다.")

with st.form("signup_form", clear_on_submit=True):
    signup_id = st.text_input("ID", placeholder="3글자 이상")
    signup_pwd = st.text_input("비밀번호", type="password", placeholder="4글자 이상")
    signup_pwd_confirm = st.text_input("비밀번호 확인", type="password")
    signup_name = st.text_input("이름")
    submitted = st.form_submit_button("회원가입", type="primary", use_container_width=True)

if submitted:
    if signup_pwd != signup_pwd_confirm:
        st.warning("비밀번호와 비밀번호 확인이 다릅니다.")
    else:
        try:
            result = signup_process(signup_id.strip(), signup_pwd, signup_name.strip())
            st.success(f"{result['name']}님, 회원가입이 완료되었습니다.")
            st.info("왼쪽 로그인 메뉴에서 새 계정으로 로그인하세요.")
        except BackendAPIError as error:
            st.error(str(error))
