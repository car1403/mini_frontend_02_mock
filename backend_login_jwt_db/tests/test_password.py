from app.core.password import hash_password, verify_password


def test_password_is_hashed_and_can_be_verified():
    password = "password123"
    saved_password = hash_password(password)

    assert saved_password != password
    assert verify_password(password, saved_password) is True
    assert verify_password("wrong-password", saved_password) is False
