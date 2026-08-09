from fastapi.testclient import TestClient
from app.main import app
from app.routers import auth_router
from app.schemes.auth_scheme import AuthPublic

client = TestClient(app)

def test_signup(monkeypatch):
    monkeypatch.setattr(auth_router, "signup_process", lambda auth: AuthPublic(id=auth.id, name=auth.name))
    response = client.post("/auth/signup", json={"id": "user01", "pwd": "password", "name": "홍길동"})
    assert response.status_code == 201
    assert response.json() == {"id": "user01", "name": "홍길동"}
