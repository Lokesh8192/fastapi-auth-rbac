from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def test_user():

    suffix = uuid4().hex[:8]

    return {
        "username": f"pytestuser_{suffix}",
        "email": f"pytest_{suffix}@example.com",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
    }


@pytest.fixture
def registered_user(test_user):

    response = client.post(
        "/auth/register",
        json=test_user,
    )

    assert response.status_code == 201

    return test_user


@pytest.fixture
def logged_in_user(registered_user):

    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200

    return response.json()["data"]


@pytest.fixture
def auth_headers(logged_in_user):

    access_token = logged_in_user["access_token"]

    return {"Authorization": f"Bearer {access_token}"}
