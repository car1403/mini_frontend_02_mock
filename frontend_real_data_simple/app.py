import streamlit as st


st.set_page_config(
    page_title="Supabase + Redis 실시간 데이터",
    page_icon="📡",
    layout="wide",
)

input_page = st.Page(
    "app_pages/real_input.py",
    title="1. 센서 입력·조회",
    icon="💾",
    default=True,
)
stream_page = st.Page(
    "app_pages/real_stream.py",
    title="2. 실시간 수신",
    icon="📡",
)

navigation = st.navigation([input_page, stream_page])
navigation.run()
