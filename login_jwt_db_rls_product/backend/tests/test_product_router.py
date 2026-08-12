from fastapi.testclient import TestClient

from app.core.auth_dependency import get_current_user
from app.main import app
from app.routers import product_router
from app.schemes.auth_scheme import CurrentUser
from app.schemes.product_scheme import ProductPublic


client = TestClient(app)


def current_user(role: str = "user") -> CurrentUser:
    return CurrentUser(
        user_id=f"{role}-uuid",
        email=f"{role}@example.com",
        role=role,
        access_token=f"{role}-token",
    )


def test_product_requires_login():
    response = client.get("/product/getall")
    assert response.status_code == 401


def test_user_can_get_all_products(monkeypatch):
    app.dependency_overrides[get_current_user] = lambda: current_user("user")
    monkeypatch.setattr(
        product_router,
        "product_get_all",
        lambda access_token: [ProductPublic(id=1, name="T-shirt", price=15000)],
    )

    try:
        response = client.get("/product/getall")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "T-shirt", "price": 15000}]


def test_user_cannot_create_product():
    app.dependency_overrides[get_current_user] = lambda: current_user("user")

    try:
        response = client.post(
            "/product/create",
            json={"name": "T-shirt", "price": 15000},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403


def test_user_cannot_update_product():
    app.dependency_overrides[get_current_user] = lambda: current_user("user")

    try:
        response = client.put(
            "/product/update/1",
            json={"name": "Updated", "price": 20000},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403


def test_user_cannot_delete_product():
    app.dependency_overrides[get_current_user] = lambda: current_user("user")

    try:
        response = client.delete("/product/delete/1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403


def test_admin_can_create_product(monkeypatch):
    app.dependency_overrides[get_current_user] = lambda: current_user("admin")
    monkeypatch.setattr(
        product_router,
        "product_create",
        lambda product, access_token, user_id: ProductPublic(
            id=1,
            name=product.name,
            price=product.price,
        ),
    )

    try:
        response = client.post(
            "/product/create",
            json={"name": "T-shirt", "price": 15000},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "T-shirt", "price": 15000}


def test_admin_can_update_product(monkeypatch):
    app.dependency_overrides[get_current_user] = lambda: current_user("admin")
    monkeypatch.setattr(
        product_router,
        "product_update",
        lambda product_id, product, access_token: ProductPublic(
            id=product_id,
            name=product.name,
            price=product.price,
        ),
    )

    try:
        response = client.put(
            "/product/update/1",
            json={"name": "Updated", "price": 20000},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


def test_admin_can_delete_product(monkeypatch):
    app.dependency_overrides[get_current_user] = lambda: current_user("admin")
    monkeypatch.setattr(
        product_router,
        "product_delete",
        lambda product_id, access_token: ProductPublic(
            id=product_id,
            name="Deleted",
            price=10000,
        ),
    )

    try:
        response = client.delete("/product/delete/1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["id"] == 1
