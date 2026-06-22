from fastapi import HTTPException, Depends
from fastapi import security
from sqlalchemy.orm import Session
from app.core.exceptions import UserNotFoundException
from app.db.dependencies import get_db
from app.models.user import User
from app.core.auth import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise UserNotFoundException()
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Admin access required!")
    return current_user
