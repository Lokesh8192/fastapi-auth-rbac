from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.db.database import init_db
from app.models.refresh_token import RefreshToken

app = FastAPI(title="FastAPI Authentication and RBAC", version="1.0.0")


@app.on_event("startup")
def on_startup():
    # Ensure DB tables exist (development convenience).
    init_db()


app.include_router(auth_router)
app.include_router(admin_router)


@app.get("/", response_model=dict)
def home():
    return {"message": "Welcome to FastAPI Authentication and RBAC"}
