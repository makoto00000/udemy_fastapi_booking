from fastapi.testclient import TestClient


def test_create(client_fixture: TestClient):
    response = client_fixture.post(
        "/room", json={"name": "room1", "capacity": 1})
    assert response.status_code == 201
    room = response.json()
    assert room["name"] == "room1"
    assert room["capacity"] == 1
