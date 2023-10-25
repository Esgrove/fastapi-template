from fastapi.testclient import TestClient

from app.main import app
from app.version import BRANCH, COMMIT, DATE, VERSION_NUMBER

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("message")


def test_version():
    response = client.get("/version/")
    assert response.status_code == 200
    data = response.json()

    assert "branch" in data
    assert "commit" in data
    assert "date" in data
    assert "version" in data

    assert data["branch"] == BRANCH
    assert data["commit"] == COMMIT
    assert data["date"] == DATE
    assert data["version"] == VERSION_NUMBER


def test_get_item():
    for item_id in (1000, 1234, 6540, 9999):
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json() == {"name": "test", "item_id": item_id}


def test_get_item_not_found():
    for item_id in (0, 1, 222, 10000):
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Item not found"}


def test_get_item_invalid_item_id():
    response = client.get("/items/abc")
    assert response.status_code == 422
    assert "detail" in response.json()


def test_list_items():
    response = client.get("/items/")
    assert response.status_code == 200


def test_list_items_parameters():
    response = client.get("/items/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
