from core.api_client import request


def signup_process(email: str, pwd: str, name: str):
    return request(
        "POST",
        "/auth/signup",
        json={"email": email, "pwd": pwd, "name": name},
    )


def login_process(email: str, pwd: str):
    return request("POST", "/auth/login", json={"email": email, "pwd": pwd})
