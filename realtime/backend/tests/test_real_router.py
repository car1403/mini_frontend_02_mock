from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_one_without_login():
    response = client.get("/real/one")

    assert response.status_code == 200
    assert response.json()["number"] == 1
    assert "temperature" in response.json()


def test_stream_without_login():
    response = client.get("/real/stream?count=1")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.text.startswith("data: ")
