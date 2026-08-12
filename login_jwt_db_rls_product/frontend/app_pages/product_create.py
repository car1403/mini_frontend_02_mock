import streamlit as st

from clients.product_client import product_insert
from core.api_client import BackendAPIError
from core.auth import is_admin, is_logged_in


st.subheader("Product 입력")

if not is_logged_in():
    st.warning("로그인이 필요합니다.")
    st.stop()

if not is_admin():
    st.warning("관리자만 상품을 입력할 수 있습니다.")
    st.stop()

with st.form("product_form", clear_on_submit=True):
    product_name = st.text_input("NAME", placeholder="상품명 입력")
    product_price = st.number_input("PRICE", min_value=0, step=1000)
    submitted = st.form_submit_button("저장")

if submitted:
    if not product_name.strip():
        st.warning("상품명을 입력해 주세요.")
    else:
        payload = {
            "name": product_name.strip(),
            "price": int(product_price),
        }

        try:
            result = product_insert(payload)
            st.success("상품 입력이 완료되었습니다.")
            st.write(result)
        except BackendAPIError as error:
            st.error(str(error))
