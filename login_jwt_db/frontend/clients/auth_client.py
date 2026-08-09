from core.api_client import request


def signup_process(id: str, pwd: str, name: str):
    return request(
        "POST",
        "/auth/signup",
        json={"id": id, "pwd": pwd, "name": name},
    )


def login_process(id: str, pwd: str):
    return request("POST", "/auth/login", json={"id": id, "pwd": pwd})
