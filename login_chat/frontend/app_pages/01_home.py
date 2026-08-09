import streamlit as st

from core.auth import is_logged_in


if is_logged_in():
    st.title(f"안녕하세요, {st.session_state.login_name}님 👋")
    st.write("로그인이 확인되었습니다. 왼쪽 메뉴에서 AI Chat을 시작하세요.")

    first, second, third = st.columns(3)
    first.metric("로그인 상태", "정상")
    second.metric("사용자 ID", st.session_state.login_id)
    third.metric("대화 수", len(st.session_state.chat_messages))

    st.info(
        "질문을 보내면 백엔드가 세션을 확인한 후 Gemini에 전달합니다. "
        "사용자 ID는 화면 입력값이 아니라 서버 세션에서 가져옵니다."
    )
else:
    st.title("로그인 후 이용하는 AI Chat")
    st.write(
        "서버 메모리 세션을 이용해 로그인한 사용자만 Gemini Chat을 사용할 수 있는 "
        "초보자용 예제입니다."
    )
    st.warning("왼쪽 로그인 메뉴에서 먼저 로그인해 주세요.")

    st.subheader("동작 흐름")
    st.code(
        "로그인 → 세션 발급 → Chat 요청 → 세션 확인 → Gemini 응답",
        language=None,
    )
