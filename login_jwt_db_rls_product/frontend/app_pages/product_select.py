import streamlit as st

from clients.product_client import (
    product_delete,
    product_select_all,
    product_update,
)
from core.api_client import BackendAPIError
from core.auth import is_admin, is_logged_in


@st.dialog("상품 삭제")
def show_delete(product: dict) -> None:
    st.write(f"{product['name']} 상품을 삭제할까요?")
    if st.button("삭제 확인"):
        try:
            product_delete(product["id"])
            st.rerun()
        except BackendAPIError as error:
            st.error(str(error))


@st.dialog("상품 수정")
def show_update(product: dict) -> None:
    with st.form(f"update_form_{product['id']}"):
        name = st.text_input("상품명", value=product["name"])
        price = st.number_input("가격", value=int(product["price"]))
        submitted = st.form_submit_button("수정")

    if submitted:
        try:
            product_update(
                product["id"],
                {"name": name, "price": int(price)},
            )
            st.rerun()
        except BackendAPIError as error:
            st.error(str(error))


st.subheader("Product 조회")

if not is_logged_in():
    st.warning("로그인이 필요합니다.")
    st.stop()

try:
    products = product_select_all()

    if not products:
        st.info("상품이 없습니다.")

    for product in products:
        with st.container(border=True):
            if is_admin():
                name_column, price_column, button_column = st.columns([2, 1, 1])
            else:
                name_column, price_column = st.columns([2, 1])

            with name_column:
                st.write(f"{product['id']} / {product['name']}")
            with price_column:
                st.write(f"{product['price']:,}원")
            # 수정·삭제 버튼은 관리자 화면에만 표시합니다.
            if is_admin():
                with button_column:
                    if st.button("수정", key=f"update_{product['id']}"):
                        show_update(product)
                    if st.button("삭제", key=f"delete_{product['id']}"):
                        show_delete(product)
except BackendAPIError as error:
    st.error(str(error))
