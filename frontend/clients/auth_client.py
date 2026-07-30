# product_client.py
# product CRUD

from typing import Any
from core.api_client import request

def login_process(id: str, pwd: str):
     return request("POST",f"/auth/login", json={"id":id, "pwd":pwd})

def logout_process(id: str):
     return request("GET",f"/auth/logout/{id}")
