from fastapi.testclient import TestClient

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