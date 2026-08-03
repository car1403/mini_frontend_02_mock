import pandas as pd
import streamlit as st

from clients.real_client import receive_real_data


st.set_page_config(
    page_title="아주 쉬운 실시간 온도",
    page_icon="🌡️",
    layout="wide",
)

st.title("가상 온도 실시간 보기")
st.caption("화면이 열리면 로그인 없이 가상 데이터 10개를 자동으로 받습니다.")

metric_box = st.empty()
table_box = st.empty()
status_box = st.empty()

received_data = []
status_box.info("백엔드 SSE에 연결하고 있습니다.")

try:
    for item in receive_real_data(count=10):
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

    status_box.success("가상 데이터 10개를 모두 받았습니다.")
except RuntimeError as error:
    status_box.error(str(error))

st.info(
    "백엔드가 한 번의 SSE 연결에서 데이터를 여러 번 보내고, "
    "프론트엔드는 데이터가 도착할 때마다 위 화면을 바꿉니다."
)
