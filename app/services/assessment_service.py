from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.constants.assessment_type import ALLOWED_ASSESSMENT_TYPES
from app.models.assessment_model import Assessment
from app.models.user_model import User
from app.repositories.assessment_repository import (
    create_assessment,
    delete_assessment,
    get_assessment_by_id,
    get_assessments,
    update_assessment,
)
from app.repositories.student_repository import get_student_by_id
from app.schemas.assessment_schema import (
    AssessmentCreateRequest,
    AssessmentListResponse,
    AssessmentUpdateRequest,
)
from app.utils.pagination import build_pagination_meta, normalize_pagination


def list_assessments(
    db: Session,
    *,
    page: int,
    limit: int,
    search: str | None = None,
    student_id: UUID | None = None,
    created_by: UUID | None = None,
    assessment_type: str | None = None,
) -> AssessmentListResponse:
    page, limit, offset = normalize_pagination(page=page, limit=limit)

    if assessment_type is not None:
        _validate_assessment_type(assessment_type)

    assessments, total = get_assessments(
        db=db,
        offset=offset,
        limit=limit,
        search=search,
        student_id=student_id,
        created_by=created_by,
        assessment_type=assessment_type,
    )

    return AssessmentListResponse(
        data=assessments,
        meta=build_pagination_meta(
            page=page,
            limit=limit,
            total=total,
        ),
    )


def get_assessment_detail(
    db: Session,
    assessment_id: int,
) -> Assessment:
    assessment = get_assessment_by_id(
        db=db,
        assessment_id=assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    return assessment


def create_new_assessment(
    db: Session,
    request: AssessmentCreateRequest,
    current_user: User,
) -> Assessment:
    student = get_student_by_id(db=db, student_id=request.student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    _validate_assessment_type(request.assessment_type)

    assessment = Assessment(
        student_id=request.student_id,
        created_by=current_user.id,
        assessment_type=request.assessment_type,
        assessment_date=request.assessment_date,
        score=request.score,
        result=request.result,
        notes=request.notes,
    )

    return create_assessment(
        db=db,
        assessment=assessment,
    )


def update_existing_assessment(
    db: Session,
    assessment_id: int,
    request: AssessmentUpdateRequest,
) -> Assessment:
    assessment = get_assessment_detail(
        db=db,
        assessment_id=assessment_id,
    )

    update_data = request.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )

    if "assessment_type" in update_data and update_data["assessment_type"] is not None:
        _validate_assessment_type(update_data["assessment_type"])

    return update_assessment(
        db=db,
        assessment=assessment,
        update_data=update_data,
    )


def delete_existing_assessment(
    db: Session,
    assessment_id: int,
) -> None:
    assessment = get_assessment_detail(
        db=db,
        assessment_id=assessment_id,
    )

    delete_assessment(
        db=db,
        assessment=assessment,
    )


def _validate_assessment_type(assessment_type: str) -> None:
    if assessment_type not in ALLOWED_ASSESSMENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid assessment type. "
                f"Allowed values: {', '.join(ALLOWED_ASSESSMENT_TYPES)}"
            ),
        )