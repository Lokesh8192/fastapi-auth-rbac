from uuid import uuid4
from datetime import UTC, datetime, timedelta

from app.models.user import User
from app.repositories.user_repository import get_user_by_email, get_user_by_username, get_user_by_id, create_user, get_users
from tests.test_database import TestingSessionLocal
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import create_refresh_token, delete_refresh_token, delete_user_refresh_tokens, get_refresh_token


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


def test_get_user_by_username():

    db = TestingSessionLocal()

    try:
        suffix = uuid4().hex[:8]

        user = User(
            username=f"pytestuser_{suffix}",
            email=f"pytest_{suffix}@example.com",
            hashed_password="hashed_password",
            role="user",
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        result = get_user_by_username(
            db=db,
            username=user.username,
        )

        assert result is not None
        assert result.id == user.id
        assert result.username == user.username
        assert result.email == user.email

    finally:
        db.delete(user)
        db.commit()
        db.close()


def test_get_user_by_username_not_found():

    db = TestingSessionLocal()

    try:
        result = get_user_by_username(
            db=db,
            username="unknown_user",
        )

        assert result is None

    finally:
        db.close()


def test_get_user_by_id():

    db = TestingSessionLocal()

    try:
        suffix = uuid4().hex[:8]

        user = User(
            username=f"pytestuser_{suffix}",
            email=f"pytest_{suffix}@example.com",
            hashed_password="hashed_password",
            role="user",
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        result = get_user_by_id(
            db=db,
            user_id=user.id,
        )

        assert result is not None
        assert result.id == user.id
        assert result.username == user.username
        assert result.email == user.email
        assert result.role == user.role
        assert result.is_active == user.is_active

    finally:
        db.delete(user)
        db.commit()
        db.close()


def test_get_user_by_id_not_found():

    db = TestingSessionLocal()

    try:
        result = get_user_by_id(
            db=db,
            user_id=999999,
        )

        assert result is None

    finally:
        db.close()


def test_create_user():

    db = TestingSessionLocal()

    try:
        suffix = uuid4().hex[:8]

        user = User(
            username=f"pytestuser_{suffix}",
            email=f"pytest_{suffix}@example.com",
            hashed_password="hashed_password",
            role="user",
            is_active=True,
        )

        created_user = create_user(
            db=db,
            user=user,
        )

        assert created_user is not None
        assert created_user.id is not None
        assert created_user.username == user.username
        assert created_user.email == user.email
        assert created_user.role == "user"
        assert created_user.is_active is True

    finally:
        db.delete(created_user)
        db.commit()
        db.close()


def test_get_users():

    db = TestingSessionLocal()

    users = []

    try:
        suffix = uuid4().hex[:8]

        user1 = User(
            username=f"user1_{suffix}",
            email=f"user1_{suffix}@example.com",
            hashed_password="password",
            role="user",
            is_active=True,
        )

        user2 = User(
            username=f"admin_{suffix}",
            email=f"admin_{suffix}@example.com",
            hashed_password="password",
            role="admin",
            is_active=False,
        )

        db.add_all([user1, user2])
        db.commit()

        users = get_users(
            db=db,
            search=None,
            role=None,
            is_active=None,
        ).all()

        assert len(users) >= 2

        usernames = [user.username for user in users]

        assert user1.username in usernames
        assert user2.username in usernames

    finally:
        db.delete(user1)
        db.delete(user2)
        db.commit()
        db.close()


def test_create_refresh_token():
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

        token = RefreshToken(
            token=f"refresh_token_{suffix}",
            user_id=user.id,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        created_token = create_refresh_token(
            db=db,
            refresh_token=token,
        )
        assert created_token is not None
        assert created_token.id is not None
        assert created_token.token is not None
        assert created_token.user_id == user.id

    finally:
        db.delete(token)
        db.delete(user)
        db.commit()
        db.close()


def test_get_refresh_token_not_found():

    db = TestingSessionLocal()

    try:
        result = get_refresh_token(
            db=db,
            token="invalid_refresh_token",
        )

        assert result is None

    finally:
        db.close()


def test_delete_refresh_token():

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

        token = RefreshToken(
            token=f"refresh_token_{suffix}",
            user_id=user.id,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        db.add(token)
        db.commit()
        db.refresh(token)
        token_value = token.token

        delete_refresh_token(
            db=db,
            refresh_token=token,
        )

        result = get_refresh_token(
            db=db,
            token=token_value,
        )

        assert result is None

    finally:
        db.delete(user)
        db.commit()
        db.close()


def test_delete_user_refresh_tokens():

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

        token1 = RefreshToken(
            token=f"refresh_token1_{suffix}",
            user_id=user.id,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        token2 = RefreshToken(
            token=f"refresh_token2_{suffix}",
            user_id=user.id,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        db.add_all([token1, token2])
        db.commit()
        token1_value = token1.token
        token2_value = token2.token

        deleted_count = delete_user_refresh_tokens(
            db=db,
            user_id=user.id,
        )

        assert deleted_count == 2

        result1 = get_refresh_token(
            db=db,
            token=token1_value,
        )

        result2 = get_refresh_token(
            db=db,
            token=token2_value,
        )

        assert result1 is None
        assert result2 is None

    finally:
        db.delete(user)
        db.commit()
        db.close()
