from uuid import uuid4

from tests.conftest import client


def test_register():
    suffix = uuid4().hex[:8]
    response = client.post(
        "/auth/register",
        json={
            "username": f"pytestuser_{suffix}",
            "email": f"pytest_{suffix}@example.com",
            "password": "Admin@123",
            "confirm_password": "Admin@123",
        },
    )
    print("\nResponse:")
    print(response.json())

    assert response.status_code == 201


def test_login():
    suffix = uuid4().hex[:8]

    email = f"login_{suffix}@example.com"
    password = "Admin@123"

    # Register user
    client.post(
        "/auth/register",
        json={
            "username": f"user_{suffix}",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    # Login user
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    print(response.json())

    assert response.status_code == 200


def test_me():
    suffix = uuid4().hex[:8]

    email = f"me_{suffix}@example.com"
    password = "Admin@123"

    # Register User
    client.post(
        "/auth/register",
        json={
            "username": f"user_{suffix}",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    # Login User
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["data"]["access_token"]

    # Call Protected Route
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    print("\n/me Response:")
    print(response.json())

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["email"] == email
    assert data["username"] == f"user_{suffix}"


def test_me_without_token():

    response = client.get("/auth/me")

    print(response.json())

    assert response.status_code == 401


def test_me_invalid_token():

    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"},
    )

    print(response.json())

    assert response.status_code == 401


def test_refresh_token():

    suffix = uuid4().hex[:8]

    email = f"refresh_{suffix}@example.com"
    password = "Admin@123"

    # Register User
    register_response = client.post(
        "/auth/register",
        json={
            "username": f"user_{suffix}",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    assert register_response.status_code == 201

    # Login User
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    # Extract Refresh Token
    refresh_token = login_response.json()["data"]["refresh_token"]

    # Generate New Access Token
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    print("\nRefresh Response:")
    print(response.json())

    assert response.status_code == 200

    data = response.json()["data"]

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_invalid_token():

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid_token"},
    )

    print("\nInvalid Refresh Token Response:")
    print(response.json())

    assert response.status_code == 401


def test_logout():

    suffix = uuid4().hex[:8]

    email = f"logout_{suffix}@example.com"
    password = "Admin@123"

    # Register
    client.post(
        "/auth/register",
        json={
            "username": f"user_{suffix}",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    refresh_token = login_response.json()["data"]["refresh_token"]

    # Logout
    response = client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token},
    )

    print("\nLogout Response:")
    print(response.json())

    assert response.status_code == 200


def test_refresh_after_logout():

    suffix = uuid4().hex[:8]

    email = f"logout_refresh_{suffix}@example.com"
    password = "Admin@123"

    # Register
    client.post(
        "/auth/register",
        json={
            "username": f"user_{suffix}",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    refresh_token = login_response.json()["data"]["refresh_token"]

    # Logout
    logout_response = client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token},
    )

    assert logout_response.status_code == 200

    # Try Refresh Again
    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    print("\nRefresh After Logout:")
    print(refresh_response.json())

    assert refresh_response.status_code == 401
