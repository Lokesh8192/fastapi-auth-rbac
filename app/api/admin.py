from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.dependencies.auth import get_current_admin
from app.models.user import User
from app.schemas.user import UserListResponse

router=APIRouter(prefix="/admin", tags=["Admin"])

@router.get(
    "/users",
    response_model=list[UserListResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    )
):

    return db.query(User).all()