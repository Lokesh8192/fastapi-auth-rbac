from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.user import User
from app.repositories.user_repository import (
    create_user as create_user_record,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.user import UserCreate
from app.utils.security import hash_password


def create_user(db: Session, user_data: UserCreate):
    logger.info(f"Registration request received for: {user_data.email}")

    existing_username = get_user_by_username(db, user_data.username)
    if existing_username:
        logger.warning(f"Username already exists: {user_data.username}")
        raise HTTPException(status_code=409, detail="Username already exists")

    existing_email = get_user_by_email(db, user_data.email)
    if existing_email:
        logger.warning(f"Email already exists: {user_data.email}")
        raise HTTPException(status_code=409, detail="Email already registered")

    try:
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

        created_user = create_user_record(db, user)

        logger.info(f"User created successfully: {created_user.email}")

        return created_user

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error while creating user")
        raise

    except Exception:
        db.rollback()
        logger.exception("Unexpected error while creating user")
        raise