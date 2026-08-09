"""JWT를 포함하여 Product API를 호출합니다."""

import streamlit as st

from core.api_client import request


def get_access_token() -> str:
    return st.session_state.get("access_token", "")


def product_insert(product: dict):
    return request(
        "POST",
        "/product/create",
        json=product,
        access_token=get_access_token(),
    )


def product_delete(product_id: int):
    return request(
        "DELETE",
        f"/product/delete/{product_id}",
        access_token=get_access_token(),
    )


def product_update(product_id: int, product: dict):
    return request(
        "PUT",
        f"/product/update/{product_id}",
        json=product,
        access_token=get_access_token(),
    )


def product_select_all():
    return request(
        "GET",
        "/product/getall",
        access_token=get_access_token(),
    )


def product_select(product_id: int):
    return request(
        "GET",
        f"/product/get/{product_id}",
        access_token=get_access_token(),
    )
