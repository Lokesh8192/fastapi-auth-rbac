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
