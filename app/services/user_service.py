from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password


def create_user(db: Session, user_data: UserCreate):
    existing_username = (
        db.query(User).filter(User.username.ilike(user_data.username)).first()
    )
    if existing_username:
        raise HTTPException(status_code=409, detail="UserName already exists!")

    existing_emil = db.query(User).filter(User.email == user_data.email).first()
    if existing_emil:
        raise HTTPException(status_code=409, detail="Email already Registered")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise
