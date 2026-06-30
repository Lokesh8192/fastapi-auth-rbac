from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import User
from app.utils.security import hash_password
from tests.test_database import TestingSessionLocal


client = TestClient(app)


@pytest.fixture
def admin_user():
    """
    Create an admin user directly in the test database.
    We do this because the register API only creates normal users.
    """

    db: Session = TestingSessionLocal()

    try:
        suffix = uuid4().hex[:8]

        admin = User(
            username=f"admin_{suffix}",
            email=f"admin_{suffix}@example.com",
            hashed_password=hash_password("Admin@123"),
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        return {
            "email": admin.email,
            "password": "Admin@123",
        }

    finally:
        db.close()

@pytest.fixture
def normal_user():

    db: Session = TestingSessionLocal()

    try:
        suffix = uuid4().hex[:8]

        user = User(
            username=f"user_{suffix}",
            email=f"user_{suffix}@example.com",
            hashed_password=hash_password("Admin@123"),
            role="user",
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()

@pytest.fixture
def search_user():
    db: Session = TestingSessionLocal()
    try:
        user = User(
            username="lokesh",
            email="lokesh@example.com",
            hashed_password=hash_password("Admin@123"),
            role="user",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    finally:
        db.close()


@pytest.fixture
def admin_headers(admin_user):
    """
    Login as admin and return Authorization header.
    """

    response = client.post(
        "/auth/login",
        json={
            "email": admin_user["email"],
            "password": admin_user["password"],
        },
    )

    assert response.status_code == 200

    access_token = response.json()["data"]["access_token"]

    return {
        "Authorization": f"Bearer {access_token}"
    }


def test_get_all_users(admin_headers):
    """
    Verify admin can retrieve all users.
    """

    response = client.get(
        "/admin/users",
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    # Verify API response
    assert body["success"] is True

    # Verify pagination fields
    assert body["page"] == 1
    assert body["size"] == 10

    # Verify response structure
    assert isinstance(body["data"], list)
    assert isinstance(body["total"], int)
    assert isinstance(body["total_pages"], int)

    # Verify keys exist
    assert "filters" in body


def test_invalid_page(admin_headers):

    response = client.get(
        "/admin/users?page=999",
        headers=admin_headers,
    )

    assert response.status_code == 404

    body = response.json()

    assert body["detail"] == "Page not found"


def test_search_users(admin_headers, search_user):

    response = client.get(
        "/admin/users/?search=lokesh",
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True

    users = body["data"]

    assert len(users) >= 1

    assert any(
        user["username"] == "lokesh"
        for user in users
    )

def test_filter_by_role(
    admin_headers,
    admin_user,
    normal_user,
):

    response = client.get(
        "/admin/users?role=admin",
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    users = body["data"]

    assert len(users) >= 1

    assert all(
        user["role"] == "admin"
        for user in users
    )