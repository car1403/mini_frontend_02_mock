import streamlit as st

from core.auth import is_logged_in


st.title("홈")

if is_logged_in():
    st.success(
        f"{st.session_state.login_name}님, "
        f"{st.session_state.user_role} 역할로 로그인했습니다."
    )
    if st.session_state.user_role == "admin":
        st.info("관리자는 Product 조회·입력·수정·삭제를 사용할 수 있습니다.")
    else:
        st.info("일반 사용자는 Product 조회만 사용할 수 있습니다.")
else:
    st.info("기능을 사용하려면 회원가입 후 로그인해 주세요.")
