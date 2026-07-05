from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import Response

from app.schemas.user import UserCreate

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.core.exception_handler import (
    global_exception_handler,
    invalid_credentials_handler,
    refresh_token_not_found_handler,
    user_not_found_handler,
    validation_exception_handler,
)
from app.core.exceptions import (
    InvalidCredentialsException,
    RefreshTokenNotFoundException,
    UserNotFoundException,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="FastAPI Authentication and RBAC",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def catch_unhandled_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return await global_exception_handler(request, exc)


app.include_router(auth_router)
app.include_router(admin_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
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
def raise_error():
    raise RuntimeError("Boom")


@app.post("/auh/rwegister")
def register_alias(user: UserCreate):
    return {"message": "ok"}
