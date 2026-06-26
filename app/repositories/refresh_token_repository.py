from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


def delete_user_refresh_tokens(
    db: Session,
    user_id: int,
):
    (
        db.query(RefreshToken)
        .filter(RefreshToken.user_id == user_id)
        .delete()
    )


def create_refresh_token(
    db: Session,
    refresh_token: RefreshToken,
):
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token


def get_refresh_token(
    db: Session,
    token: str,
):
    return (
        db.query(RefreshToken)
        .filter(RefreshToken.token == token)
        .first()
    )


def delete_refresh_token(
    db: Session,
    refresh_token: RefreshToken,
):
    db.delete(refresh_token)
    db.commit()