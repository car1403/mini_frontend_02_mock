from core.api_client import request


def login_process(id: str, pwd: str):
    return request("POST", "/auth/login", json={"id": id, "pwd": pwd})
