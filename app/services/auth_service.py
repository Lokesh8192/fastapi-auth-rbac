from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidCredentialsException, RefreshTokenNotFoundException, UserNotFoundException
from app.models.user import User
from app.models.refresh_token import RefreshToken

from app.schemas.user import LoginRequest

from app.utils.security import verify_password

from app.core.auth import create_access_token, create_refresh_token, decode_access_token

from app.core.config import settings


def login_user(db: Session, login_data: LoginRequest):

    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise UserNotFoundException()
    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise InvalidCredentialsException()

    # Generate Access Token
    access_token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )

    # Generate Refresh Token
    refresh_token = create_refresh_token({"sub": str(user.id)})

    try:

        # Optional:
        # Remove old refresh tokens for this user
        db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()

        # Save new refresh token
        refresh_record = RefreshToken(
            token=refresh_token,
            user_id=user.id,
            expires_at=(
                datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            ),
        )

        db.add(refresh_record)

        db.commit()

    except Exception:

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


def refresh_access_token(db: Session, refresh_token: str):
    payload = decode_access_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    token_type = payload.get("type")
    if token_type != "refresh":
        raise HTTPException(status_code=401, detail="Invali token type")
    db_token = (
        db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token).first()
    )

    if not db_token:
        raise RefreshTokenNotFoundException()
    user = db.query(User).filter(User.id == db_token.user_id).first()

    if not user:
        raise UserNotFoundException()
    access_token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}


def logout_user(db: Session, refresh_token: str):

    token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token).first()

    if not token:
        raise RefreshTokenNotFoundException()

    db.delete(token)

    db.commit()

    return {"message": "Logout successful"}
