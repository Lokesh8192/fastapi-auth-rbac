from pydantic import BaseModel, EmailStr, field_validator, Field, model_validator
import re
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Username")
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("password must contain at least 8 characters")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one upper case letter")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lower case letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*]", value):
            raise ValueError("Password must contain at least one special character")

        return value

    @model_validator(mode="after")
    def validate_confirm_password(self):

        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class LoginUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    user: LoginUserResponse
    access_token: str
    token: TokenResponse


class UserListResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


class PaginatedUserListResponse(BaseModel):
    success: bool
    page: int
    size: int
    total: int
    total_pages: int
    data: list[UserListResponse]


class RefreshTokenRequest(BaseModel):
    refresh_token: str
