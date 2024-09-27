from fastapi.testclient import TestClient


def test_create(client_fixture: TestClient):
    response = client_fixture.post("/user", json={"name": "test1"})
    assert response.status_code == 201
    user = response.json()
    assert user["name"] == "test1"
