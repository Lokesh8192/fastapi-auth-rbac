from fastapi import HTTPException
import pytest
from app.core.exceptions import UserNotFoundException, InvalidCredentialsException, RefreshTokenNotFoundException
from unittest.mock import MagicMock, patch

from app.schemas.user import LoginRequest
from app.services.auth_service import login_user, refresh_access_token, logout_user


@patch("app.services.auth_service.create_refresh_token_record")
@patch("app.services.auth_service.delete_user_refresh_tokens")
@patch("app.services.auth_service.create_refresh_token")
@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_user_by_email")
def test_login_user_success(
    mock_get_user_by_email,
    mock_verify_password,
    mock_create_access_token,
    mock_create_refresh_token,
    mock_delete_user_refresh_tokens,
    mock_create_refresh_token_record,
):
    db = MagicMock()

    login_data = LoginRequest(
        email="lokesh@example.com",
        password="Admin@123",
    )

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.username = "lokesh"
    fake_user.email = "lokesh@example.com"
    fake_user.hashed_password = "hashed_password"
    fake_user.role = "user"
    fake_user.is_active = True

    mock_get_user_by_email.return_value = fake_user
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "fake_access_token"
    mock_create_refresh_token.return_value = "fake_refresh_token"
    mock_delete_user_refresh_tokens.return_value = 1
    mock_create_refresh_token_record.return_value = MagicMock()

    result = login_user(
        db=db,
        login_data=login_data,
    )

    assert result["access_token"] == "fake_access_token"
    assert result["refresh_token"] == "fake_refresh_token"
    assert result["token_type"] == "bearer"

    assert result["user"]["id"] == fake_user.id
    assert result["user"]["username"] == fake_user.username
    assert result["user"]["email"] == fake_user.email
    assert result["user"]["role"] == fake_user.role
    assert result["user"]["is_active"] == fake_user.is_active

    mock_get_user_by_email.assert_called_once_with(
        db,
        login_data.email,
    )

    mock_verify_password.assert_called_once_with(
        login_data.password,
        fake_user.hashed_password,
    )

    mock_create_access_token.assert_called_once_with(
        {
            "sub": str(fake_user.id),
            "email": fake_user.email,
            "role": fake_user.role,
        }
    )

    mock_create_refresh_token.assert_called_once_with(
        {"sub": str(fake_user.id)}
    )

    mock_delete_user_refresh_tokens.assert_called_once_with(
        db,
        fake_user.id,
    )

    mock_create_refresh_token_record.assert_called_once()
    
@patch("app.services.auth_service.create_refresh_token_record")
@patch("app.services.auth_service.delete_user_refresh_tokens")
@patch("app.services.auth_service.create_refresh_token")
@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_user_by_email")
def test_login_user_user_not_found(
    mock_get_user_by_email,
    mock_verify_password,
    mock_create_access_token,
    mock_create_refresh_token,
    mock_delete_user_refresh_tokens,
    mock_create_refresh_token_record,
):
    db = MagicMock()

    login_data = LoginRequest(
        email="unknown@example.com",
        password="Admin@123",
    )

    mock_get_user_by_email.return_value = None

    with pytest.raises(UserNotFoundException):
        login_user(
            db=db,
            login_data=login_data,
        )

    mock_get_user_by_email.assert_called_once_with(
        db,
        login_data.email,
    )

    mock_verify_password.assert_not_called()
    mock_create_access_token.assert_not_called()
    mock_create_refresh_token.assert_not_called()
    mock_delete_user_refresh_tokens.assert_not_called()
    mock_create_refresh_token_record.assert_not_called()
    
@patch("app.services.auth_service.create_refresh_token_record")
@patch("app.services.auth_service.delete_user_refresh_tokens")
@patch("app.services.auth_service.create_refresh_token")
@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_user_by_email")
def test_login_user_invalid_password(
    mock_get_user_by_email,
    mock_verify_password,
    mock_create_access_token,
    mock_create_refresh_token,
    mock_delete_user_refresh_tokens,
    mock_create_refresh_token_record,
):
    db = MagicMock()

    login_data = LoginRequest(
        email="lokesh@example.com",
        password="WrongPassword@123",
    )

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.email = "lokesh@example.com"
    fake_user.hashed_password = "hashed_password"

    mock_get_user_by_email.return_value = fake_user
    mock_verify_password.return_value = False

    with pytest.raises(InvalidCredentialsException):
        login_user(
            db=db,
            login_data=login_data,
        )

    mock_get_user_by_email.assert_called_once_with(
        db,
        login_data.email,
    )

    mock_verify_password.assert_called_once_with(
        login_data.password,
        fake_user.hashed_password,
    )

    mock_create_access_token.assert_not_called()
    mock_create_refresh_token.assert_not_called()
    mock_delete_user_refresh_tokens.assert_not_called()
    mock_create_refresh_token_record.assert_not_called()
    
@patch("app.services.auth_service.create_refresh_token_record")
@patch("app.services.auth_service.delete_user_refresh_tokens")
@patch("app.services.auth_service.create_refresh_token")
@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_user_by_email")
def test_login_user_repository_exception(
    mock_get_user_by_email,
    mock_verify_password,
    mock_create_access_token,
    mock_create_refresh_token,
    mock_delete_user_refresh_tokens,
    mock_create_refresh_token_record,
):
    db = MagicMock()

    login_data = LoginRequest(
        email="lokesh@example.com",
        password="Admin@123",
    )

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.username = "lokesh"
    fake_user.email = "lokesh@example.com"
    fake_user.hashed_password = "hashed_password"
    fake_user.role = "user"
    fake_user.is_active = True

    mock_get_user_by_email.return_value = fake_user
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "fake_access_token"
    mock_create_refresh_token.return_value = "fake_refresh_token"

    mock_create_refresh_token_record.side_effect = Exception(
        "Database Error"
    )

    with pytest.raises(Exception, match="Database Error"):
        login_user(
            db=db,
            login_data=login_data,
        )

    mock_get_user_by_email.assert_called_once_with(
        db,
        login_data.email,
    )

    mock_verify_password.assert_called_once_with(
        login_data.password,
        fake_user.hashed_password,
    )

    mock_delete_user_refresh_tokens.assert_called_once_with(
        db,
        fake_user.id,
    )

    mock_create_refresh_token_record.assert_called_once()

    db.rollback.assert_called_once()

@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.get_user_by_id")
@patch("app.services.auth_service.get_refresh_token")
@patch("app.services.auth_service.decode_access_token")
def test_refresh_access_token_success(
    mock_decode_access_token,
    mock_get_refresh_token,
    mock_get_user_by_id,
    mock_create_access_token,
):
    db = MagicMock()

    refresh_token = "fake_refresh_token"

    fake_payload = {
        "sub": "1",
        "type": "refresh",
    }

    fake_db_token = MagicMock()
    fake_db_token.user_id = 1

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.email = "lokesh@example.com"
    fake_user.role = "user"

    mock_decode_access_token.return_value = fake_payload
    mock_get_refresh_token.return_value = fake_db_token
    mock_get_user_by_id.return_value = fake_user
    mock_create_access_token.return_value = "new_access_token"

    result = refresh_access_token(
        db=db,
        refresh_token=refresh_token,
    )

    assert result["access_token"] == "new_access_token"
    assert result["token_type"] == "bearer"

    mock_decode_access_token.assert_called_once_with(
        refresh_token
    )

    mock_get_refresh_token.assert_called_once_with(
        db,
        refresh_token,
    )

    mock_get_user_by_id.assert_called_once_with(
        db,
        fake_db_token.user_id,
    )

    mock_create_access_token.assert_called_once_with(
        {
            "sub": str(fake_user.id),
            "email": fake_user.email,
            "role": fake_user.role,
        }
    )

@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.get_user_by_id")
@patch("app.services.auth_service.get_refresh_token")
@patch("app.services.auth_service.decode_access_token")
def test_refresh_access_token_invalid_token(
    mock_decode_access_token,
    mock_get_refresh_token,
    mock_get_user_by_id,
    mock_create_access_token,
):
    db = MagicMock()

    refresh_token = "invalid_refresh_token"

    mock_decode_access_token.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        refresh_access_token(
            db=db,
            refresh_token=refresh_token,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid refresh token"

    mock_decode_access_token.assert_called_once_with(
        refresh_token
    )

    mock_get_refresh_token.assert_not_called()
    mock_get_user_by_id.assert_not_called()
    mock_create_access_token.assert_not_called()

@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.get_user_by_id")
@patch("app.services.auth_service.get_refresh_token")
@patch("app.services.auth_service.decode_access_token")
def test_refresh_access_token_invalid_type(
    mock_decode_access_token,
    mock_get_refresh_token,
    mock_get_user_by_id,
    mock_create_access_token,
):
    db = MagicMock()

    refresh_token = "access_token_used_as_refresh_token"

    mock_decode_access_token.return_value = {
        "sub": "1",
        "type": "access",
    }

    with pytest.raises(HTTPException) as exc_info:
        refresh_access_token(
            db=db,
            refresh_token=refresh_token,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token type"

    mock_decode_access_token.assert_called_once_with(
        refresh_token
    )

    mock_get_refresh_token.assert_not_called()
    mock_get_user_by_id.assert_not_called()
    mock_create_access_token.assert_not_called()
    
@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.get_user_by_id")
@patch("app.services.auth_service.get_refresh_token")
@patch("app.services.auth_service.decode_access_token")
def test_refresh_access_token_not_found(
    mock_decode_access_token,
    mock_get_refresh_token,
    mock_get_user_by_id,
    mock_create_access_token,
):
    db = MagicMock()

    refresh_token = "valid_but_deleted_refresh_token"

    mock_decode_access_token.return_value = {
        "sub": "1",
        "type": "refresh",
    }

    mock_get_refresh_token.return_value = None

    with pytest.raises(RefreshTokenNotFoundException):
        refresh_access_token(
            db=db,
            refresh_token=refresh_token,
        )

    mock_decode_access_token.assert_called_once_with(
        refresh_token
    )

    mock_get_refresh_token.assert_called_once_with(
        db,
        refresh_token,
    )

    mock_get_user_by_id.assert_not_called()
    mock_create_access_token.assert_not_called()

@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.get_user_by_id")
@patch("app.services.auth_service.get_refresh_token")
@patch("app.services.auth_service.decode_access_token")
def test_refresh_access_token_user_not_found(
    mock_decode_access_token,
    mock_get_refresh_token,
    mock_get_user_by_id,
    mock_create_access_token,
):
    db = MagicMock()

    refresh_token = "valid_refresh_token"

    fake_db_token = MagicMock()
    fake_db_token.user_id = 999

    mock_decode_access_token.return_value = {
        "sub": "999",
        "type": "refresh",
    }

    mock_get_refresh_token.return_value = fake_db_token
    mock_get_user_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        refresh_access_token(
            db=db,
            refresh_token=refresh_token,
        )

    mock_decode_access_token.assert_called_once_with(
        refresh_token
    )

    mock_get_refresh_token.assert_called_once_with(
        db,
        refresh_token,
    )

    mock_get_user_by_id.assert_called_once_with(
        db,
        fake_db_token.user_id,
    )

    mock_create_access_token.assert_not_called()

@patch("app.services.auth_service.delete_refresh_token")
@patch("app.services.auth_service.get_refresh_token")
def test_logout_user_success(
    mock_get_refresh_token,
    mock_delete_refresh_token,
):
    db = MagicMock()

    refresh_token = "valid_refresh_token"

    fake_db_token = MagicMock()
    fake_db_token.user_id = 1

    mock_get_refresh_token.return_value = fake_db_token

    result = logout_user(
        db=db,
        refresh_token=refresh_token,
    )

    assert result == {
        "message": "Logout successful"
    }

    mock_get_refresh_token.assert_called_once_with(
        db,
        refresh_token,
    )

    mock_delete_refresh_token.assert_called_once_with(
        db,
        fake_db_token,
    )

@patch("app.services.auth_service.delete_refresh_token")
@patch("app.services.auth_service.get_refresh_token")
def test_logout_user_token_not_found(
    mock_get_refresh_token,
    mock_delete_refresh_token,
):
    db = MagicMock()

    refresh_token = "invalid_refresh_token"

    mock_get_refresh_token.return_value = None

    with pytest.raises(RefreshTokenNotFoundException):
        logout_user(
            db=db,
            refresh_token=refresh_token,
        )

    mock_get_refresh_token.assert_called_once_with(
        db,
        refresh_token,
    )

    mock_delete_refresh_token.assert_not_called()