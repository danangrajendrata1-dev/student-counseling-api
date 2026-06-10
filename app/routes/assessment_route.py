from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.constants.roles import ADMIN, COUNSELOR
from app.core.dependencies import require_roles
from app.database import get_db
from app.models.user_model import User
from app.schemas.assessment_schema import (
    AssessmentCreateRequest,
    AssessmentDetailResponse,
    AssessmentListResponse,
    AssessmentResponse,
    AssessmentUpdateRequest,
)
from app.services.assessment_service import (
    create_new_assessment,
    delete_existing_assessment,
    get_assessment_detail,
    list_assessments,
    update_existing_assessment,
)

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.get("", response_model=AssessmentListResponse)
def get_assessments_route(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    student_id: UUID | None = Query(default=None),
    created_by: UUID | None = Query(default=None),
    assessment_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> AssessmentListResponse:
    return list_assessments(
        db=db,
        page=page,
        limit=limit,
        search=search,
        student_id=student_id,
        created_by=created_by,
        assessment_type=assessment_type,
    )

@router.post(
    "",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_assessment_route(
    request: AssessmentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> AssessmentResponse:
    return create_new_assessment(
        db=db,
        request=request,
        current_user=current_user,
    )


@router.get("/{assessment_id}", response_model=AssessmentDetailResponse)
def get_assessment_detail_route(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> AssessmentDetailResponse:
    assessment = get_assessment_detail(
        db=db,
        assessment_id=assessment_id,
    )

    return AssessmentDetailResponse(data=assessment)


@router.patch("/{assessment_id}", response_model=AssessmentResponse)
def update_assessment_route(
    assessment_id: int,
    request: AssessmentUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> AssessmentResponse:
    return update_existing_assessment(
        db=db,
        assessment_id=assessment_id,
        request=request,
    )


@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assessment_route(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> None:
    delete_existing_assessment(
        db=db,
        assessment_id=assessment_id,
    )