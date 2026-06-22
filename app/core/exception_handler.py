from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import InvalidCredentialsException, RefreshTokenNotFoundException, UserNotFoundException


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )

async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsException,
):
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def refresh_token_not_found_handler(
    request: Request,
    exc: RefreshTokenNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )

async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )