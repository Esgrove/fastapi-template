from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_item():
    for item_id in (1, 1000, 354):
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json() == {"name": "test", "item_id": item_id}


def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
