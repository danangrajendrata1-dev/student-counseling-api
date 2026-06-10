from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check() -> dict:
    settings = get_settings()

    return {
        "status": "ok",
        "message": f"{settings.app_name} is running",
        "version": settings.app_version,
        "environment": settings.app_env,
    }