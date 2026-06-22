from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.dependencies.auth import get_current_admin
from app.models.user import User
from app.schemas.user import PaginatedUserListResponse
import math

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=PaginatedUserListResponse)
def get_all_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: str | None = None,
    role: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    query = db.query(User)
    if search:
        query = query.filter(User.username.ilike(f"%{search}%"))
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    total_users = db.query(User).count()
    total_pages = math.ceil(total_users / size) if total_users > 0 else 1

    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")

    offset = (page - 1) * size

    users = db.query(User).offset(offset).limit(size).all()

    return {
        "success": True,
        "page": page,
        "size": size,
        "total": total_users,
        "total_pages": total_pages,
        "filters": {
            "search": search,
            "role": role,
            "is_active": is_active,
        },
        "data": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
            }
            for user in users
        ],
    }
