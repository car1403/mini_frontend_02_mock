import streamlit as st

from core.auth import is_logged_in


st.title("홈")

if is_logged_in():
    st.success(
        f"{st.session_state.login_name}님"
        f"({st.session_state.login_id}) 로그인 상태입니다."
    )
    st.info("왼쪽 메뉴에서 로그인 이후 기능을 사용할 수 있습니다.")
else:
    st.info("기능을 사용하려면 회원가입 후 로그인해 주세요.")
