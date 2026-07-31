import pandas as pd
import streamlit as st

from clients.real_client import receive_real_data
from core.api_client import BackendAPIError
from core.auth import is_logged_in


st.title("가상 온도 실시간 보기")
st.caption("버튼을 누르면 백엔드가 1초마다 새로운 가상 온도를 보냅니다.")

if not is_logged_in():
    st.warning("먼저 로그인해 주세요.")
    st.stop()

count = st.slider("받을 데이터 개수", min_value=3, max_value=20, value=10)

metric_box = st.empty()
table_box = st.empty()
status_box = st.empty()

if st.button("실시간 데이터 받기", type="primary"):
    received_data = []
    status_box.info("백엔드에 연결했습니다. 데이터를 기다리는 중입니다.")

    try:
        for item in receive_real_data(count):
            received_data.insert(0, item)

            metric_box.metric(
                label=f"{item['created_at']} 현재 온도",
                value=f"{item['temperature']}℃",
                delta=item["status"],
            )
            table_box.dataframe(
                pd.DataFrame(received_data),
                use_container_width=True,
                hide_index=True,
            )

        status_box.success(f"가상 데이터 {len(received_data)}개를 모두 받았습니다.")
    except BackendAPIError as error:
        status_box.error(str(error))

st.info(
    "화면 전체를 새로고침하는 것이 아니라, SSE 연결에서 데이터가 도착할 때마다 "
    "metric과 표의 내용을 바꾸고 있습니다."
)
