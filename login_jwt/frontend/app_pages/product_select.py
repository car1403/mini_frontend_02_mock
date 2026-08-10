"""상품 목록을 조회하고 수정·삭제할 수 있는 화면입니다."""

import streamlit as st

from clients.product_client import (
    product_delete,
    product_select_all,
    product_update,
)
from core.api_client import BackendAPIError
from core.auth import is_logged_in


@st.dialog("상품 삭제")
def show_delete(product: dict) -> None:
    """선택한 상품을 정말 삭제할지 확인하는 팝업을 엽니다."""

    st.write(f"{product['name']} 상품을 삭제할까요?")
    if st.button("삭제 확인"):
        try:
            product_delete(product["id"])
            # 삭제 결과를 반영한 목록을 다시 그리기 위해 화면을 재실행합니다.
            st.rerun()
        except BackendAPIError as error:
            st.error(str(error))


@st.dialog("상품 수정")
def show_update(product: dict) -> None:
    """기존 상품 정보를 수정하는 입력 팝업을 엽니다."""

    # 상품마다 다른 form key를 사용하여 Streamlit 위젯 이름 충돌을 방지합니다.
    with st.form(f"update_form_{product['id']}"):
        name = st.text_input("상품명", value=product["name"])
        price = st.number_input("가격", value=int(product["price"]))
        submitted = st.form_submit_button("수정")

    if submitted:
        try:
            # 수정할 상품 ID는 URL로, 이름과 가격은 JSON Body로 전송됩니다.
            product_update(
                product["id"],
                {"name": name, "price": int(price)},
            )
            st.rerun()
        except BackendAPIError as error:
            st.error(str(error))


st.subheader("Product 조회")

if not is_logged_in():
    # 메뉴를 우회해 직접 접근한 경우에도 상품 API 화면을 보호합니다.
    st.warning("로그인이 필요합니다.")
    st.stop()

try:
    # API 클라이언트가 session_state의 JWT를 Authorization 헤더에 담아 요청합니다.
    products = product_select_all()

    if not products:
        st.info("상품이 없습니다.")

    for product in products:
        # 상품 하나마다 테두리가 있는 영역과 세 개의 열을 만듭니다.
        with st.container(border=True):
            name_column, price_column, button_column = st.columns([2, 1, 1])

            with name_column:
                st.write(f"{product['id']} / {product['name']}")
            with price_column:
                st.write(f"{product['price']:,}원")
            with button_column:
                if st.button("수정", key=f"update_{product['id']}"):
                    show_update(product)
                if st.button("삭제", key=f"delete_{product['id']}"):
                    show_delete(product)
except BackendAPIError as error:
    st.error(str(error))
