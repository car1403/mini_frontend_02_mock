import time

import pandas as pd
import streamlit as st

from clients.real_client import receive_real_data
from core.api_client import BackendAPIError
from core.auth import is_logged_in


st.title("2. Redis 실시간 수신")
st.caption("Upstash Redis에 발행된 새 데이터를 SSE로 받습니다.")

if not is_logged_in():
    st.warning("먼저 로그인해 주세요.")
    st.stop()

receive_seconds = st.slider(
    "수신 시간(초)",
    min_value=10,
    max_value=60,
    value=20,
)

status_box = st.empty()
metric_box = st.empty()
table_box = st.empty()

st.info(
    "수신을 시작한 다음 다른 브라우저 탭의 `1. 센서 데이터 입력·조회` 화면에서 "
    "데이터를 입력하세요."
)

if st.button("실시간 수신 시작", type="primary"):
    received = []
    stream_error = False
    started_at = time.time()
    status_box.info("Redis 이벤트를 기다리고 있습니다.")

    try:
        for event_name, item in receive_real_data():
            if event_name == "heartbeat":
                if time.time() - started_at >= receive_seconds:
                    break
                continue

            if event_name == "error":
                stream_error = True
                status_box.error(item.get("error", "Redis 연결 오류가 발생했습니다."))
                break

            received.insert(0, item)
            metric_box.metric(
                f"{item['device_name']} 현재 온도",
                f"{item['temperature']}℃",
                f"습도 {item['humidity']}%",
            )
            table_box.dataframe(
                pd.DataFrame(received),
                use_container_width=True,
                hide_index=True,
            )

            if time.time() - started_at >= receive_seconds:
                break

        if not stream_error:
            status_box.success(
                f"수신을 종료했습니다. 새 데이터 {len(received)}개를 받았습니다."
            )
    except BackendAPIError as error:
        status_box.error(str(error))
