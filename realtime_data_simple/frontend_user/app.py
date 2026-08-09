import streamlit as st


# 사용자 화면의 브라우저 탭 제목과 기본 화면 모양을 설정합니다.
st.set_page_config(
    page_title="실시간 센서 데이터",
    page_icon="📡",
    layout="wide",
)

# 사용자는 Redis를 통해 전달되는 실시간 센서 데이터를 확인합니다.
user_page = st.Page(
    "app_pages/real_stream.py",
    title="실시간 센서 데이터",
    icon="📡",
    default=True,
)

navigation = st.navigation([user_page])
navigation.run()
