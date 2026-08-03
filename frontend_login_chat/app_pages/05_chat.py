import streamlit as st

from clients.chat_client import send_chat
from core.api_client import BackendAPIError
from core.auth import is_logged_in


if not is_logged_in():
    st.warning("로그인이 필요합니다.")
    st.stop()

st.title("💬 AI Chat")
st.caption(f"{st.session_state.login_name}님과 Gemini의 대화")

if not st.session_state.chat_messages:
    st.info("아래 입력창에 첫 질문을 입력해 보세요.")

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    st.session_state.chat_messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gemini가 답변을 만들고 있습니다..."):
            try:
                result = send_chat(
                    prompt,
                    st.session_state.session_token,
                )
                answer = result["answer"]
                st.markdown(answer)
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": answer}
                )
            except BackendAPIError as error:
                st.error(str(error))
