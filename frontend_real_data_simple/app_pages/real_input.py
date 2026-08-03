import streamlit as st

from core.api_client import BackendAPIError, create_real_data, get_recent_real_data


st.title("1. 센서 데이터 입력·조회")
st.caption("입력하면 Supabase에 저장되고 Upstash Redis로도 발행됩니다.")

with st.form("real_data_form", clear_on_submit=True):
    device_name = st.text_input("장치 이름", value="sensor-01")
    temperature = st.number_input("온도", value=25.0, step=0.1)
    humidity = st.number_input(
        "습도",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=0.1,
    )
    submitted = st.form_submit_button("Supabase 저장 + Redis 발행")

if submitted:
    try:
        result = create_real_data(
            {
                "device_name": device_name,
                "temperature": temperature,
                "humidity": humidity,
            }
        )
        if result["event_published"]:
            st.success("Supabase 저장과 Redis 발행이 완료되었습니다.")
        else:
            st.warning("Supabase 저장은 완료됐지만 Redis 발행에는 실패했습니다.")
        st.json(result)
    except BackendAPIError as error:
        st.error(str(error))

st.divider()

if st.button("Supabase 최근 데이터 조회"):
    try:
        rows = get_recent_real_data()
        st.dataframe(rows, use_container_width=True, hide_index=True)
    except BackendAPIError as error:
        st.error(str(error))

st.info(
    "실시간 수신을 확인하려면 다른 브라우저 탭에서 `2. 실시간 수신`을 먼저 연 뒤, "
    "이 화면에서 데이터를 입력하세요."
)
