from core.api_client import request


def login_process(id: str, pwd: str):
    return request("POST", "/auth/login", json={"id": id, "pwd": pwd})


def logout_process(session_token: str):
    return request(
        "POST",
        "/auth/logout",
        session_token=session_token,
    )
