from fastapi.testclient import TestClient
from schemas import BookingValidationMessages


# 正常系
def test_create(client_fixture: TestClient):
    data = {
        "reserved_num": 1,
        "start_date_time": "2020-01-01T09:00:00",
        "end_date_time": "2020-01-01T12:00:00",
    }
    user_id = 1
    room_id = 1
    response = client_fixture.post(
        f"/booking?user_id={user_id}&room_id={room_id}", json=data)
    assert response.status_code == 201
    booking = response.json()
    assert booking["reserved_num"] == 1
    assert booking["start_date_time"] == "2020-01-01T09:00:00"
    assert booking["end_date_time"] == "2020-01-01T12:00:00"
    assert booking["user_id"] == 1
    assert booking["room_id"] == 1


# 部屋の定員を超えているとき
def test_create_over_capacity(client_fixture: TestClient):
    data = {
        "reserved_num": 2,
        "start_date_time": "2020-01-01T09:00:00",
        "end_date_time": "2020-01-01T12:00:00",
    }
    user_id = 1
    room_id = 1
    response = client_fixture.post(
        f"/booking?user_id={user_id}&room_id={room_id}", json=data)
    assert response.status_code == 422
    assert response.json()["detail"] == (
        BookingValidationMessages.OVER_CAPACITY.value)


# 時間が15分刻みでないとき
def test_create_invalid_minute(client_fixture: TestClient):
    data = {
        "reserved_num": 1,
        "start_date_time": "2020-01-01T09:01:00",
        "end_date_time": "2020-01-01T12:00:00",
    }
    user_id = 1
    room_id = 1
    response = client_fixture.post(
        f"/booking?user_id={user_id}&room_id={room_id}", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0] == (
        BookingValidationMessages.INVALID_MINUTE.value)


# 時間が9:00~20:00でないとき
def test_create_out_of_hours(client_fixture: TestClient):
    data = {
        "reserved_num": 1,
        "start_date_time": "2020-01-01T09:00:00",
        "end_date_time": "2020-01-01T21:00:00",
    }
    user_id = 1
    room_id = 1
    response = client_fixture.post(
        f"/booking?user_id={user_id}&room_id={room_id}", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0] == (
        BookingValidationMessages.OUT_OF_HOURS.value)


# 予約日が2日にまたいだとき
def test_create_different_days(client_fixture: TestClient):
    data = {
        "reserved_num": 1,
        "start_date_time": "2020-01-01T09:00:00",
        "end_date_time": "2020-01-02T12:00:00",
    }
    user_id = 1
    room_id = 1
    response = client_fixture.post(
        f"/booking?user_id={user_id}&room_id={room_id}", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0] == (
        BookingValidationMessages.DIFFERENT_DAYS.value)


# 開始時間と終了時間が逆転したとき
def test_create_start_after_end(client_fixture: TestClient):
    data = {
        "reserved_num": 1,
        "start_date_time": "2020-01-01T12:00:00",
        "end_date_time": "2020-01-01T09:00:00",
    }
    user_id = 1
    room_id = 1
    response = client_fixture.post(
        f"/booking?user_id={user_id}&room_id={room_id}", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0] == (
        BookingValidationMessages.START_AFTER_END.value)
