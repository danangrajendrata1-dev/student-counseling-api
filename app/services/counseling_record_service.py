from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.constants.counseling_status import ALLOWED_COUNSELING_STATUSES
from app.models.counseling_record_model import CounselingRecord
from app.models.user_model import User
from app.repositories.counseling_record_repository import (
    create_counseling_record,
    delete_counseling_record,
    get_counseling_record_by_id,
    get_counseling_records,
    update_counseling_record,
)
from app.repositories.student_repository import get_student_by_id
from app.schemas.counseling_record_schema import (
    CounselingRecordCreateRequest,
    CounselingRecordListResponse,
    CounselingRecordUpdateRequest,
)
from app.utils.pagination import build_pagination_meta, normalize_pagination


def list_counseling_records(
    db: Session,
    *,
    page: int,
    limit: int,
    search: str | None = None,
    student_id: UUID | None = None,
    counselor_id: UUID | None = None,
    record_status: str | None = None,
) -> CounselingRecordListResponse:
    page, limit, offset = normalize_pagination(page=page, limit=limit)

    if record_status is not None:
        _validate_counseling_status(record_status)

    records, total = get_counseling_records(
        db=db,
        offset=offset,
        limit=limit,
        search=search,
        student_id=student_id,
        counselor_id=counselor_id,
        status=record_status,
    )

    return CounselingRecordListResponse(
        data=records,
        meta=build_pagination_meta(
            page=page,
            limit=limit,
            total=total,
        ),
    )


def get_counseling_record_detail(
    db: Session,
    counseling_record_id: int,
) -> CounselingRecord:
    counseling_record = get_counseling_record_by_id(
        db=db,
        counseling_record_id=counseling_record_id,
    )

    if counseling_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counseling record not found",
        )

    return counseling_record


def create_new_counseling_record(
    db: Session,
    request: CounselingRecordCreateRequest,
    current_user: User,
) -> CounselingRecord:
    student = get_student_by_id(db=db, student_id=request.student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    _validate_counseling_status(request.status)

    counseling_record = CounselingRecord(
        student_id=request.student_id,
        counselor_id=current_user.id,
        counseling_date=request.counseling_date,
        topic=request.topic,
        description=request.description,
        follow_up=request.follow_up,
        status=request.status,
    )

    return create_counseling_record(
        db=db,
        counseling_record=counseling_record,
    )


def update_existing_counseling_record(
    db: Session,
    counseling_record_id: int,
    request: CounselingRecordUpdateRequest,
) -> CounselingRecord:
    counseling_record = get_counseling_record_detail(
        db=db,
        counseling_record_id=counseling_record_id,
    )

    update_data = request.model_dump(exclude_unset=True)

    if "status" in update_data:
        _validate_counseling_status(update_data["status"])

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )

    return update_counseling_record(
        db=db,
        counseling_record=counseling_record,
        update_data=update_data,
    )


def delete_existing_counseling_record(
    db: Session,
    counseling_record_id: int,
) -> None:
    counseling_record = get_counseling_record_detail(
        db=db,
        counseling_record_id=counseling_record_id,
    )

    delete_counseling_record(
        db=db,
        counseling_record=counseling_record,
    )


def _validate_counseling_status(record_status: str) -> None:
    if record_status not in ALLOWED_COUNSELING_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid counseling record status. "
                f"Allowed values: {', '.join(ALLOWED_COUNSELING_STATUSES)}"
            ),
        )