import streamlit as st

from core.api_client import BackendAPIError, receive_real_data


st.title("실시간 센서 데이터")
st.caption("관리자가 전송한 새 센서 데이터를 실시간으로 확인하는 화면입니다.")

status_box = st.empty()
metric_box = st.empty()
table_box = st.empty()

st.info(
    "수신을 시작하면 새 센서 데이터를 계속 기다립니다. "
    "수신을 끝내려면 브라우저를 새로고침하거나 탭을 닫으세요."
)

if st.button("실시간 수신 시작", type="primary"):
    received_data_list = []
    status_box.info("새 센서 데이터를 기다리고 있습니다.")

    try:
        # receive_real_data()는 서버에서 이벤트가 올 때마다 값을 하나씩 반환합니다.
        for event_name, received_data in receive_real_data():
            if event_name == "error":
                status_box.error(
                    received_data.get("error", "실시간 연결 오류가 발생했습니다.")
                )
                break

            # 새 데이터를 목록 맨 앞에 넣어 최신 데이터부터 보여 줍니다.
            received_data_list.insert(0, received_data)
            metric_box.metric(
                f"{received_data['device_name']} 현재 온도",
                f"{received_data['temperature']}℃",
                f"습도 {received_data['humidity']}%",
            )
            table_box.dataframe(
                received_data_list,
                use_container_width=True,
                hide_index=True,
            )
    except BackendAPIError as error:
        status_box.error(str(error))
