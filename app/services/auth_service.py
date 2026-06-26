from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, create_refresh_token, decode_access_token
from app.core.config import settings
from app.core.exceptions import InvalidCredentialsException, RefreshTokenNotFoundException, UserNotFoundException
from app.core.logger import logger
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import (
    create_refresh_token as create_refresh_token_record,
    delete_refresh_token,
    delete_user_refresh_tokens,
    get_refresh_token,
)
from app.repositories.user_repository import get_user_by_email, get_user_by_id
from app.schemas.user import LoginRequest
from app.utils.security import verify_password


def login_user(db: Session, login_data: LoginRequest):
    logger.info(f"Login attempt: {login_data.email}")
    user = get_user_by_email(db, login_data.email)

    if not user:
        logger.warning(f"User not found: {login_data.email}")
        raise UserNotFoundException()

    if not verify_password(login_data.password, user.hashed_password):
        logger.warning(f"Invalid password attempt: {login_data.email}")
        raise InvalidCredentialsException()

    logger.info(f"Login successful: {user.email}")
    access_token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = create_refresh_token({"sub": str(user.id)})

    try:
        delete_user_refresh_tokens(db, user.id)
        refresh_record = RefreshToken(
            token=refresh_token,
            user_id=user.id,
            expires_at=(
                datetime.now(UTC) +
                timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            ),
        )

        create_refresh_token_record(db, refresh_record)
        logger.info(f"Refresh token generated for user: {user.email}")
    except Exception as exc:
        logger.error(f"Database error during login: {exc}")
        db.rollback()
        raise

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token(
    db: Session,
    refresh_token: str,
):
    logger.info("Refresh token request received")

    payload = decode_access_token(refresh_token)

    if not payload:
        logger.warning("Invalid refresh token")
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    token_type = payload.get("type")

    if token_type != "refresh":
        logger.warning("Invalid token type")
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    db_token = get_refresh_token(db, refresh_token)

    if not db_token:
        logger.warning("Refresh token not found")
        raise RefreshTokenNotFoundException()

    user = get_user_by_id(db, db_token.user_id)

    if not user:
        logger.warning("User not found for refresh token")
        raise UserNotFoundException()

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    logger.info(f"Access token refreshed for user: {user.email}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


def logout_user(
    db: Session,
    refresh_token: str,
):
    logger.info("Logout request received")

    token = get_refresh_token(db, refresh_token)

    if not token:
        logger.warning("Refresh token not found during logout")
        raise RefreshTokenNotFoundException()

    user_id = token.user_id

    delete_refresh_token(db, token)

    logger.info(f"User logged out successfully. User ID: {user_id}")

    return {"message": "Logout successful"}
