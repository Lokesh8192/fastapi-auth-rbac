from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import (
    create_user as create_user_record,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.user import UserCreate
from app.utils.security import hash_password


def create_user(db: Session, user_data: UserCreate):
    existing_username = get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already exists")

    existing_email = get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    try:
        return create_user_record(db, user)
    except Exception:
        db.rollback()
        raise
