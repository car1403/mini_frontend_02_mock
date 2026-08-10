"""현재 로그인 상태에 맞는 안내를 보여 주는 홈 화면입니다."""

import streamlit as st

from core.auth import is_logged_in


st.title("홈")

if is_logged_in():
    # session_state에 저장된 로그인 ID를 화면에 표시합니다.
    st.success(f"{st.session_state.login_id} 로그인 상태입니다.")
    st.info("왼쪽 메뉴에서 Product 조회와 입력 기능을 사용할 수 있습니다.")
else:
    # JWT가 없는 사용자는 보호된 Product 기능을 사용할 수 없습니다.
    st.info("Product 기능을 사용하려면 먼저 로그인해 주세요.")
