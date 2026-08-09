import random
import time

import streamlit as st

from core.api_client import BackendAPIError, create_real_data, get_recent_real_data


st.title("센서 데이터 관리")
st.caption("관리자가 센서 데이터를 입력하고 최근 저장 데이터를 조회하는 화면입니다.")

# form 안의 입력값은 전송 버튼을 눌렀을 때 한 번에 처리됩니다.
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
    submitted = st.form_submit_button("센서 데이터 전송")

if submitted:
    try:
        saved_data = create_real_data(
            {
                "device_name": device_name,
                "temperature": temperature,
                "humidity": humidity,
            }
        )

        # event_published 값으로 Redis 실시간 전송 성공 여부를 구분합니다.
        if saved_data["event_published"]:
            st.success("데이터를 저장하고 사용자 화면으로 실시간 전송했습니다.")
        else:
            st.warning("데이터는 저장했지만 실시간 전송에는 실패했습니다.")

        st.json(saved_data)
    except BackendAPIError as error:
        st.error(str(error))

st.divider()

st.subheader("자동 센서 데이터 전송")
st.caption(
    "임의의 온도와 습도를 만들고 설정한 개수만큼 주기적으로 전송합니다."
)

auto_device_name = st.text_input(
    "자동 전송 장치 이름",
    value="auto-sensor-01",
)
send_interval = st.slider(
    "전송 주기(초)",
    min_value=1,
    max_value=30,
    value=5,
)
send_count = st.slider(
    "전송 개수",
    min_value=1,
    max_value=20,
    value=5,
)

if st.button("자동 전송 시작", type="primary"):
    sent_data_list = []
    progress_bar = st.progress(0)
    status_box = st.empty()

    # 설정한 전송 개수만큼 반복합니다.
    for index in range(send_count):
        # 온도는 15~35도, 습도는 30~80% 사이에서 무작위로 만듭니다.
        random_sensor_data = {
            "device_name": auto_device_name,
            "temperature": round(random.uniform(15.0, 35.0), 1),
            "humidity": round(random.uniform(30.0, 80.0), 1),
        }

        try:
            saved_data = create_real_data(random_sensor_data)
            sent_data_list.insert(0, saved_data)
            progress_bar.progress((index + 1) / send_count)
            status_box.info(
                f"{index + 1}/{send_count}개 전송 완료"
            )
        except BackendAPIError as error:
            st.error(f"자동 전송 실패: {error}")
            break

        # 마지막 데이터를 보낸 뒤에는 더 기다릴 필요가 없습니다.
        if index < send_count - 1:
            time.sleep(send_interval)

    if sent_data_list:
        status_box.success(f"자동 전송을 마쳤습니다. 총 {len(sent_data_list)}개 전송")
        st.dataframe(sent_data_list, use_container_width=True, hide_index=True)

st.divider()

if st.button("최근 데이터 조회"):
    try:
        recent_data = get_recent_real_data()
        st.dataframe(recent_data, use_container_width=True, hide_index=True)
    except BackendAPIError as error:
        st.error(str(error))

st.info(
    "실시간 전송을 확인하려면 사용자 화면에서 `실시간 수신 시작`을 먼저 누른 뒤 "
    "이 화면에서 데이터를 전송하세요."
)
