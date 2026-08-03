from app.core.password import hash_password, verify_password

def test_password_hash_and_verify():
    saved_password = hash_password("password123")
    assert saved_password != "password123"
    assert verify_password("password123", saved_password) is True
    assert verify_password("wrong", saved_password) is False
