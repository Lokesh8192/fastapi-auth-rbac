from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.dependencies import get_db
from tests.test_database import TestingSessionLocal
from sqlalchemy import text


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

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


@pytest.fixture(autouse=True)
def cleanup_database():

    yield

    db = TestingSessionLocal()

    try:
        db.execute(text("TRUNCATE TABLE refresh_tokens RESTART IDENTITY CASCADE"))
        db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
        db.commit()
    finally:
        db.close()
