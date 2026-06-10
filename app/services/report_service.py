from sqlalchemy.orm import Session

from app.constants.counseling_status import IN_PROGRESS, OPEN, RESOLVED
from app.constants.student_status import ACTIVE
from app.repositories.report_repository import (
    count_assessments,
    count_counseling_records,
    count_counseling_records_by_status,
    count_students,
    count_students_by_status,
    get_assessments_grouped_by_type,
    get_counseling_records_grouped_by_status,
)
from app.schemas.report_schema import ReportSummaryResponse


def get_report_summary(db: Session) -> ReportSummaryResponse:
    total_students = count_students(db=db)
    active_students = count_students_by_status(
        db=db,
        student_status=ACTIVE,
    )

    total_counseling_records = count_counseling_records(db=db)
    open_counseling_records = count_counseling_records_by_status(
        db=db,
        record_status=OPEN,
    )
    in_progress_counseling_records = count_counseling_records_by_status(
        db=db,
        record_status=IN_PROGRESS,
    )
    resolved_counseling_records = count_counseling_records_by_status(
        db=db,
        record_status=RESOLVED,
    )

    total_assessments = count_assessments(db=db)

    counseling_records_by_status = get_counseling_records_grouped_by_status(db=db)
    assessments_by_type = get_assessments_grouped_by_type(db=db)

    return ReportSummaryResponse(
        total_students=total_students,
        active_students=active_students,
        total_counseling_records=total_counseling_records,
        open_counseling_records=open_counseling_records,
        in_progress_counseling_records=in_progress_counseling_records,
        resolved_counseling_records=resolved_counseling_records,
        total_assessments=total_assessments,
        counseling_records_by_status=counseling_records_by_status,
        assessments_by_type=assessments_by_type,
    )