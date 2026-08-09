import hashlib
import hmac
import secrets


ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 200_000


def hash_password(password: str) -> str:
    """비밀번호를 복원할 수 없는 해시 문자열로 변환합니다."""

    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        ITERATIONS,
    ).hex()

    return f"{ALGORITHM}${ITERATIONS}${salt}${password_hash}"


def verify_password(password: str, saved_password: str) -> bool:
    """입력 비밀번호와 DB에 저장된 해시를 비교합니다."""

    try:
        algorithm, iterations, salt, expected_hash = saved_password.split("$")

        if algorithm != ALGORITHM:
            return False

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations),
        ).hex()
        return hmac.compare_digest(actual_hash, expected_hash)
    except (ValueError, TypeError):
        return False
