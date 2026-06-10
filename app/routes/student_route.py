from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.constants.roles import ADMIN, COUNSELOR
from app.core.dependencies import require_roles
from app.database import get_db
from app.models.user_model import User
from app.schemas.student_schema import (
    StudentCreateRequest,
    StudentDetailResponse,
    StudentListResponse,
    StudentResponse,
    StudentUpdateRequest,
)
from app.services.student_service import (
    create_new_student,
    delete_existing_student,
    get_student_detail,
    list_students,
    update_existing_student,
)


router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", response_model=StudentListResponse)
def get_student_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    class_name: str | None = Query(default=None),
    major: str | None = Query(default=None),
    academic_year: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
):
    return list_students(
        db,
        page=page,
        limit=limit,
        search=search,
        class_name=class_name,
        major=major,
        academic_year=academic_year,
        status_filter=status_filter,
    )


@router.post(
    "",
    response_model=StudentDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    payload: StudentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
):
    return create_new_student(db, payload)


@router.get("/{student_id}", response_model=StudentDetailResponse)
def get_student(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
):
    return get_student_detail(db, student_id)


@router.patch("/{student_id}", response_model=StudentResponse)
def update_student_route(
    student_id: UUID,
    request: StudentUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> StudentResponse:
    return update_existing_student(
        db=db,
        student_id=student_id,
        request=request,
    )


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_route(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN)),
) -> None:
    delete_existing_student(
        db=db,
        student_id=student_id,
    )