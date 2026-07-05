from uuid import uuid4

from app.models.user import User
from app.repositories.user_repository import get_user_by_email
from tests.test_database import TestingSessionLocal


def test_get_user_by_email():

    db = TestingSessionLocal()

    try:
        suffix = uuid4().hex[:8]

        user = User(
            username=f"user_{suffix}",
            email=f"user_{suffix}@example.com",
            hashed_password="hashed_password",
            role="user",
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        result = get_user_by_email(
            db=db,
            email=user.email,
        )

        assert result is not None
        assert result.id == user.id
        assert result.email == user.email
        assert result.username == user.username

    finally:
        db.delete(user)
        db.commit()
        db.close()

def test_get_user_by_email_not_found():

    db = TestingSessionLocal()

    try:
        result = get_user_by_email(
            db=db,
            email="doesnotexist@example.com",
        )

        assert result is None

    finally:
        db.close()