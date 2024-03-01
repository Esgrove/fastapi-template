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


def test_create_item():
    names = ("test1", "test2", "test3", "test4")
    ids = (1000, 1234, 6540, 9999)
    for name, item_id in zip(names, ids):
        new_item = {"name": name, "item_id": item_id}
        response = client.post("/items/", json=new_item)
        assert response.status_code == 201
        assert response.json() == {"name": name, "item_id": item_id}


def test_get_item():
    for item_id in (1000, 1234, 6540, 9999):
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "item_id" in data
        assert data.get("item_id") == item_id


def test_get_item_incorrect_id():
    for item_id in (0, 1, 222, 999, 10000):
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 400
        assert response.json() == {"message": "Item ID must be be between 1000 and 9999"}


def test_get_item_invalid_item_id():
    response = client.get("/items/abc")
    assert response.status_code == 422
    assert "detail" in response.json()


def test_list_items():
    response = client.get("/items/")
    assert response.status_code == 200


def test_list_items_parameters():
    for limit in (1, 3, 5):
        response = client.get(f"/items/?limit={limit}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == limit
