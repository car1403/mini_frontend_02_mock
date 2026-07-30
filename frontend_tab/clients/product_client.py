# product_client.py
# product CRUD

from typing import Any
from core.api_client import request

def product_insert():
    ""

def product_delete(product_id: int):
    # JSON
    return request("DELETE",f"/product/delete/{product_id}")

def product_update():
    ""

def product_select_all():
    return request("GET",f"/product/getall")

def product_select(product_id: int):
    return request("GET",f"/product/get/{product_id}")