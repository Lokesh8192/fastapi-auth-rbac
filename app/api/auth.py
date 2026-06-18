from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse,LoginRequest
from app.services.user_service import create_user
from app.services.auth_service import login_user
from app.schemas.common import ApiResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=ApiResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    created_user = create_user(db=db, user_data=user)

    return ApiResponse(
        success=True,
        message="User Registered Successfully",
        data=UserResponse.model_validate(created_user),
    )

@router.post("/login",response_model=ApiResponse,status_code=200)
def login(login_data:LoginRequest, db:Session=Depends(get_db)):
    result=login_user(db=db,login_data=login_data)
    
    return ApiResponse(
        success=True,
        message="Login Successful",
        data=result
    )
    
@router.get("/me")
def get_me(Current_user:UserResponse=Depends(get_current_user)):
    return ApiResponse(
        success=True,
        message="Current User Retrieved Successfully",
        data=UserResponse.model_validate(Current_user)
    )