from core.api_client import request


def send_chat(prompt: str, session_token: str):
    return request(
        "POST",
        "/chat/gemini",
        json={"prompt": prompt},
        session_token=session_token,
    )
