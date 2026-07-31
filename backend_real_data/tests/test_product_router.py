from fastapi.testclient import TestClient

from app.main import app
from app.routers import product_router
from app.schemes.product_scheme import ProductPublic


client = TestClient(app)


def login_headers() -> dict[str, str]:
    response = client.post("/auth/login", json={"id": "id01", "pwd": "pwd01"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_login_returns_jwt():
    response = client.post("/auth/login", json={"id": "id01", "pwd": "pwd01"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_product_requires_login():
    response = client.get("/product/getall")

    assert response.status_code == 401


def test_product_rejects_wrong_token():
    response = client.get(
        "/product/getall",
        headers={"Authorization": "Bearer wrong-token"},
    )

    assert response.status_code == 401


def test_product_get_all_after_login(monkeypatch):
    products = [ProductPublic(id=1, name="T-shirt", price=15000)]
    monkeypatch.setattr(product_router, "product_get_all", lambda: products)

    response = client.get("/product/getall", headers=login_headers())

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "T-shirt", "price": 15000}]
