from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.constants.roles import ADMIN, COUNSELOR, PRINCIPAL
from app.core.dependencies import require_roles
from app.database import get_db
from app.models.user_model import User
from app.schemas.report_schema import ReportSummaryResponse
from app.services.report_service import get_report_summary

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary", response_model=ReportSummaryResponse)
def get_report_summary_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR, PRINCIPAL)),
) -> ReportSummaryResponse:
    return get_report_summary(db=db)