from fastapi import APIRouter, Depends

from app.constants.roles import ADMIN, COUNSELOR, PRINCIPAL
from app.core.dependencies import require_roles
from app.models.user_model import User

router = APIRouter(
    prefix="/debug/permissions",
    tags=["Debug Permissions"],
)


@router.get("/admin-only")
def admin_only(
    current_user: User = Depends(require_roles(ADMIN)),
) -> dict:
    return {
        "message": "Admin access granted",
        "user_id": current_user.id,
        "role": current_user.role,
    }


@router.get("/admin-or-counselor")
def admin_or_counselor(
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> dict:
    return {
        "message": "Admin or counselor access granted",
        "user_id": current_user.id,
        "role": current_user.role,
    }


@router.get("/report-access")
def report_access(
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR, PRINCIPAL)),
) -> dict:
    return {
        "message": "Report access granted",
        "user_id": current_user.id,
        "role": current_user.role,
    }