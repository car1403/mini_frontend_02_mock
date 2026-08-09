import streamlit as st


# 관리자 화면의 브라우저 탭 제목과 기본 화면 모양을 설정합니다.
st.set_page_config(
    page_title="센서 데이터 관리자",
    page_icon="💾",
    layout="wide",
)

# 관리자는 센서 데이터를 입력하고 최근 저장 데이터를 조회합니다.
admin_page = st.Page(
    "app_pages/real_input.py",
    title="센서 데이터 관리",
    icon="💾",
    default=True,
)

navigation = st.navigation([admin_page])
navigation.run()
