from fastapi.testclient import TestClient

from __PACKAGE__.main import app

client = TestClient(app)


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_item_roundtrip():
    assert client.post("/api/v1/items", json={"id": 1, "name": "a"}).status_code == 201
    assert client.post("/api/v1/items", json={"id": 1, "name": "a"}).status_code == 409
    assert client.get("/api/v1/items/1").json()["name"] == "a"
    assert client.get("/api/v1/items/2").status_code == 404
