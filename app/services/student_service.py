from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.constants.student_status import ALLOWED_STUDENT_STATUSES
from app.repositories.student_repository import (
    create_student,
    delete_student,
    get_student_by_id,
    get_student_by_nis,
    get_students,
    update_student,
)
from app.schemas.student_schema import StudentCreateRequest, StudentUpdateRequest
from app.utils.pagination import build_pagination_meta, normalize_pagination


def list_students(
    db: Session,
    *,
    page: int,
    limit: int,
    search: str | None,
    class_name: str | None,
    major: str | None,
    academic_year: str | None,
    status_filter: str | None,
) -> dict:
    safe_page, safe_limit, offset = normalize_pagination(page, limit)

    if status_filter and status_filter not in ALLOWED_STUDENT_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student status",
        )

    students, total = get_students(
        db,
        search=search,
        class_name=class_name,
        major=major,
        academic_year=academic_year,
        status=status_filter,
        offset=offset,
        limit=safe_limit,
    )

    return {
        "message": "Students fetched successfully",
        "data": students,
        "pagination": build_pagination_meta(safe_page, safe_limit, total),
    }


def get_student_detail(db: Session, student_id: UUID) -> dict:
    student = get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return {
        "message": "Student fetched successfully",
        "data": student,
    }


def create_new_student(db: Session, payload: StudentCreateRequest) -> dict:
    if payload.status not in ALLOWED_STUDENT_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student status",
        )

    existing_student = get_student_by_nis(db, payload.nis)

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="NIS already registered",
        )

    student = create_student(db, payload.model_dump())

    return {
        "message": "Student created successfully",
        "data": student,
    }


def update_existing_student(
    db: Session,
    student_id: UUID,
    request: StudentUpdateRequest,
):
    student = get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    update_data = request.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )

    if "status" in update_data and update_data["status"] not in ALLOWED_STUDENT_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student status",
        )

    if "nis" in update_data:
        existing_student = get_student_by_nis(db, update_data["nis"])

        if existing_student and existing_student.id != student.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="NIS already registered",
            )

    return update_student(db, student, update_data)

def delete_existing_student(db: Session, student_id: UUID) -> dict:
    student = get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    delete_student(db, student)

    return {
        "message": "Student deleted successfully",
        "data": None,
    }