from fastapi import FastAPI
from starlette.routing import Router
from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.db.database import init_db
from app.models.refresh_token import RefreshToken
from app.core.exceptions import InvalidCredentialsException, RefreshTokenNotFoundException, UserNotFoundException
from app.core.exception_handler import (
    invalid_credentials_handler,
    refresh_token_not_found_handler,
    user_not_found_handler,
)
from app.core.exception_handler import global_exception_handler

app = FastAPI(title="FastAPI Authentication and RBAC", version="1.0.0")


@app.on_event("startup")
def on_startup():
    # Ensure DB tables exist (development convenience).
    init_db()


app.include_router(auth_router)
app.include_router(admin_router)
app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler,
)
app.add_exception_handler(
    InvalidCredentialsException,
    invalid_credentials_handler,
)
app.add_exception_handler(
    RefreshTokenNotFoundException,
    refresh_token_not_found_handler,
)
app.add_exception_handler(
    Exception,
    global_exception_handler,
)


@app.get("/", response_model=dict)
def home():
    return {"message": "Welcome to FastAPI Authentication and RBAC"}


@app.get("/error")
def test_error():
    return 10 / 0
