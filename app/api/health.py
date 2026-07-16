from fastapi import APIRouter

router=APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("/")
def health_check():
    return{
        "status": "healthy",
        "application": "FastAPI Auth RBAC",
        "version": "1.0.0",
    }