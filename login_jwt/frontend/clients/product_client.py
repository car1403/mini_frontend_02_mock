"""JWT를 포함하여 Product API를 호출합니다."""

import streamlit as st

from core.api_client import request


def get_access_token() -> str:
    """로그인할 때 session_state에 저장한 JWT를 가져옵니다."""

    return st.session_state.get("access_token", "")


def product_insert(product: dict):
    """JWT와 상품 정보를 보내 새 상품을 생성합니다."""

    return request(
        "POST",
        "/product/create",
        json=product,
        access_token=get_access_token(),
    )


def product_delete(product_id: int):
    """JWT를 포함하여 지정한 ID의 상품 삭제를 요청합니다."""

    return request(
        "DELETE",
        f"/product/delete/{product_id}",
        access_token=get_access_token(),
    )


def product_update(product_id: int, product: dict):
    """JWT와 수정할 상품 정보를 백엔드에 보냅니다."""

    return request(
        "PUT",
        f"/product/update/{product_id}",
        json=product,
        access_token=get_access_token(),
    )


def product_select_all():
    """JWT를 포함하여 전체 상품 목록을 요청합니다."""

    return request(
        "GET",
        "/product/getall",
        access_token=get_access_token(),
    )


def product_select(product_id: int):
    """JWT를 포함하여 상품 한 개를 요청합니다."""

    return request(
        "GET",
        f"/product/get/{product_id}",
        access_token=get_access_token(),
    )
