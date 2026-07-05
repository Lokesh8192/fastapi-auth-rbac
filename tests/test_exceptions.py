from fastapi.testclient import TestClient
from app.core.auth import create_refresh_token

from app.main import app

client = TestClient(app)


def test_user_not_found():

    response = client.post(
        "/auth/login",
        json={
            "email": "nouser@example.com",
            "password": "Admin@123",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == "User not found"


def test_invalid_password(registered_user):

    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401

    body = response.json()

    assert body["success"] is False
    assert body["message"] == "Invalid credentials"


def test_invalid_refresh_token():
    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": "invalid_token"
        }
    )

    assert response.status_code == 401

    body = response.json()

    assert body["detail"] == "Invalid refresh token"


def test_refresh_token_not_found():

    refresh_token = create_refresh_token(
        {"sub": "999"}
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )
    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False

    assert body["message"] == "Refresh token not found"


def test_validation_error():
    response = client.post(
        "/auh/rwegister",
        json={
            "username": "lokesh",
            "email": "lokesh@gmail.com",
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert "detail" in body


def test_global_exception_handler():

    response = client.get("/error")

    assert response.status_code == 500

    body = response.json()

    assert body["success"] is False

    assert body["message"] == "Internal Server Error"
