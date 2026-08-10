"""로그인한 사용자가 새 상품 정보를 입력하는 화면입니다."""

import streamlit as st

from clients.product_client import product_insert
from core.api_client import BackendAPIError
from core.auth import is_logged_in


st.subheader("Product 입력")

if not is_logged_in():
    # 직접 URL로 접근하더라도 로그인하지 않았다면 아래 화면 실행을 중단합니다.
    st.warning("로그인이 필요합니다.")
    st.stop()

# 폼 안의 값을 저장 버튼을 누를 때 한 번에 처리합니다.
with st.form("product_form", clear_on_submit=True):
    product_id = st.number_input("ID", min_value=1, step=1)
    product_name = st.text_input("NAME", placeholder="상품명 입력")
    product_price = st.number_input("PRICE", min_value=0, step=1000)
    submitted = st.form_submit_button("저장")

if submitted:
    # 공백만 입력한 상품명도 빈 상품명으로 처리합니다.
    if not product_name.strip():
        st.warning("상품명을 입력해 주세요.")
    else:
        # 화면 입력값을 백엔드 Product API가 요구하는 딕셔너리로 만듭니다.
        payload = {
            "id": int(product_id),
            "name": product_name.strip(),
            "price": int(product_price),
        }

        try:
            # product_insert()가 JWT를 포함하여 보호된 백엔드 API를 호출합니다.
            result = product_insert(payload)
            st.success("상품 입력이 완료되었습니다.")
            st.write(result)
        except BackendAPIError as error:
            st.error(str(error))
