"""회원가입 입력 폼을 연습하는 화면입니다. 현재는 DB에 저장하지 않습니다."""

import streamlit as st


st.title("📝 회원가입")
st.write("회원 정보를 입력해 주세요.")

# clear_on_submit=True이므로 전송 후 입력칸을 비웁니다.
with st.form("signup_form", clear_on_submit=True):
    signup_id = st.text_input(
        "ID",
        placeholder="사용할 ID를 입력하세요",
    )
    signup_pwd = st.text_input(
        "PWD",
        type="password",
        placeholder="사용할 비밀번호를 입력하세요",
    )
    signup_name = st.text_input(
        "이름",
        placeholder="이름을 입력하세요",
    )
    signup_submitted = st.form_submit_button(
        "회원가입",
        type="primary",
        use_container_width=True,
    )

if signup_submitted:
    # 필수 입력값 중 하나라도 비어 있으면 회원가입을 처리하지 않습니다.
    if not signup_id or not signup_pwd or not signup_name:
        st.warning("ID, PWD, 이름을 모두 입력해 주세요.")
    else:
        # 이 예제에는 회원가입 백엔드가 없어 성공 메시지만 보여 줍니다.
        st.success(f"{signup_name}님, 회원가입 정보가 입력되었습니다.")
