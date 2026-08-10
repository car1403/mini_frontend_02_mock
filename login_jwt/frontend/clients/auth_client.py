"""인증과 관련된 백엔드 API 호출을 모아 둔 파일입니다."""

from core.api_client import request


def login_process(id: str, pwd: str):
    """아이디와 비밀번호를 JSON으로 보내고 로그인 결과를 반환합니다."""

    return request("POST", "/auth/login", json={"id": id, "pwd": pwd})
