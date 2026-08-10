"""JWT 로그인과 상품 API 보호가 올바른지 확인하는 테스트입니다."""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import product_router
from app.schemes.product_scheme import ProductPublic


client = TestClient(app)


def login_headers() -> dict[str, str]:
    """로그인 후 보호된 API 호출에 사용할 Authorization 헤더를 만듭니다."""

    response = client.post("/auth/login", json={"id": "id01", "pwd": "pwd01"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_login_returns_jwt():
    # 올바른 계정으로 로그인하면 bearer 방식의 JWT가 반환되어야 합니다.
    response = client.post("/auth/login", json={"id": "id01", "pwd": "pwd01"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_product_requires_login():
    # JWT 없이 상품 API를 호출하면 로그인이 필요하므로 401이어야 합니다.
    response = client.get("/product/getall")

    assert response.status_code == 401


def test_product_rejects_wrong_token():
    # 서버가 만든 토큰이 아닌 임의 문자열도 401로 거절해야 합니다.
    response = client.get(
        "/product/getall",
        headers={"Authorization": "Bearer wrong-token"},
    )

    assert response.status_code == 401


def test_product_get_all_after_login(monkeypatch):
    # 서비스의 고정 예제 대신 테스트용 상품을 반환하도록 함수를 잠시 교체합니다.
    products = [ProductPublic(id=1, name="T-shirt", price=15000)]
    monkeypatch.setattr(product_router, "product_get_all", lambda: products)

    response = client.get("/product/getall", headers=login_headers())

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "T-shirt", "price": 15000}]
