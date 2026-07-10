from unittest.mock import MagicMock, patch
from fastapi import HTTPException

import pytest

from app.schemas.user import UserCreate
from app.services.user_service import create_user


@patch("app.services.user_service.create_user_record")
@patch("app.services.user_service.hash_password")
@patch("app.services.user_service.get_user_by_email")
@patch("app.services.user_service.get_user_by_username")
def test_create_user_success(
    mock_get_username,
    mock_get_email,
    mock_hash_password,
    mock_create_user,
):
    db = MagicMock()

    user_data = UserCreate(
        username="lokesh",
        email="lokesh@example.com",
        password="Admin@123",
        confirm_password="Admin@123",
    )

    mock_get_username.return_value = None
    mock_get_email.return_value = None
    mock_hash_password.return_value = "hashed_password"

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.username = user_data.username
    fake_user.email = user_data.email

    mock_create_user.return_value = fake_user

    result = create_user(db, user_data)

    assert result == fake_user

    mock_get_username.assert_called_once_with(db, user_data.username)
    mock_get_email.assert_called_once_with(db, user_data.email)
    mock_hash_password.assert_called_once_with(user_data.password)
    mock_create_user.assert_called_once()


@patch("app.services.user_service.get_user_by_username")
def test_create_user_duplicate_username(mock_get_username):

    db = MagicMock()

    user_data = UserCreate(
        username="lokesh",
        email="lokesh@example.com",
        password="Admin@123",
        confirm_password="Admin@123",
    )

    mock_get_username.return_value = MagicMock()

    with pytest.raises(HTTPException) as exc:

        create_user(db, user_data)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Username already exists"

    mock_get_username.assert_called_once_with(
        db,
        user_data.username,
    )


@patch("app.services.user_service.create_user_record")
@patch("app.services.user_service.hash_password")
@patch("app.services.user_service.get_user_by_email")
@patch("app.services.user_service.get_user_by_username")
def test_create_user_duplicate_email(
    mock_get_username,
    mock_get_email,
    mock_hash_password,
    mock_create_user,
):
    db = MagicMock()

    user_data = UserCreate(
        username="lokesh",
        email="lokesh@example.com",
        password="Admin@123",
        confirm_password="Admin@123",
    )

    # Username is available
    mock_get_username.return_value = None

    # Email already exists
    mock_get_email.return_value = MagicMock()

    with pytest.raises(HTTPException) as exc:
        create_user(db, user_data)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Email already registered"

    mock_get_username.assert_called_once_with(
        db,
        user_data.username,
    )

    mock_get_email.assert_called_once_with(
        db,
        user_data.email,
    )

    # These should never be called
    mock_hash_password.assert_not_called()
    mock_create_user.assert_not_called()


@patch("app.services.user_service.create_user_record")
@patch("app.services.user_service.hash_password")
@patch("app.services.user_service.get_user_by_email")
@patch("app.services.user_service.get_user_by_username")
def test_create_user_repository_exception(
    mock_get_username,
    mock_get_email,
    mock_hash_password,
    mock_create_user,
):
    db = MagicMock()

    user_data = UserCreate(
        username="lokesh",
        email="lokesh@example.com",
        password="Admin@123",
        confirm_password="Admin@123",
    )

    mock_get_username.return_value = None
    mock_get_email.return_value = None
    mock_hash_password.return_value = "hashed_password"

    mock_create_user.side_effect = Exception("Database Error")

    with pytest.raises(Exception, match="Database Error"):
        create_user(db, user_data)

    db.rollback.assert_called_once()

    mock_create_user.assert_called_once()
