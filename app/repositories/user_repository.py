from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_username(
    db: Session,
    username: str,
):
    return (
        db.query(User)
        .filter(User.username.ilike(username))
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int,
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def create_user(
    db: Session,
    user: User,
):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(
    db: Session,
    search: str | None,
    role: str | None,
    is_active: bool | None,
):
    query = db.query(User)

    if search:
        query = query.filter(User.username.ilike(f"%{search}%"))

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query