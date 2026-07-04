from app.core.auth import create_access_token
from app.models.user import User
from tests.conftest import client
from tests.test_database import TestingSessionLocal


def test_register(test_user):
    response = client.post("/auth/register", json=test_user)

    assert response.status_code == 201


def test_registered_user_fixture(registered_user):
    assert registered_user["email"] is not None


def test_logged_in_user_fixture(logged_in_user):
    assert "access_token" in logged_in_user
    assert "refresh_token" in logged_in_user


def test_auth_headers_fixture(auth_headers):
    assert "Authorization" in auth_headers


def test_get_current_user(auth_headers, registered_user):
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["data"]["email"] == registered_user["email"]


def test_refresh_token(logged_in_user):
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": logged_in_user["refresh_token"]},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "access_token" in response.json()["data"]


def test_logout(logged_in_user):
    response = client.post(
        "/auth/logout",
        json={"refresh_token": logged_in_user["refresh_token"]},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_regular_user_cannot_access_admin_endpoint(auth_headers):
    response = client.get("/admin/users", headers=auth_headers)

    assert response.status_code == 403


def test_invalid_access_token_returns_401():
    invalid_token = create_access_token({"sub": "1"})[:-3]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 401


def test_non_numeric_subject_in_token_returns_401():
    token = create_access_token({"sub": "not-a-number"})

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_admin_users_respects_filters(registered_user):
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == registered_user["email"]).first()
        user.role = "admin"
        db.commit()
    finally:
        db.close()

    login_response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    token = login_response.json()["data"]["access_token"]

    response = client.get(
        "/admin/users?role=admin&page=1&size=10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["filters"]["role"] == "admin"
    assert response.json()["data"][0]["email"] == registered_user["email"]
