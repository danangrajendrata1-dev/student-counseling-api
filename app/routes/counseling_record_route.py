from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.constants.roles import ADMIN, COUNSELOR
from app.core.dependencies import get_current_user, require_roles
from app.database import get_db
from app.models.user_model import User
from app.schemas.counseling_record_schema import (
    CounselingRecordCreateRequest,
    CounselingRecordDetailResponse,
    CounselingRecordListResponse,
    CounselingRecordResponse,
    CounselingRecordUpdateRequest,
)
from app.services.counseling_record_service import (
    create_new_counseling_record,
    delete_existing_counseling_record,
    get_counseling_record_detail,
    list_counseling_records,
    update_existing_counseling_record,
)

router = APIRouter(prefix="/counseling-records", tags=["Counseling Records"])


@router.get("", response_model=CounselingRecordListResponse)
def get_counseling_records_route(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    student_id: UUID | None = Query(default=None),
    counselor_id: UUID | None = Query(default=None),
    status_query: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> CounselingRecordListResponse:
    return list_counseling_records(
        db=db,
        page=page,
        limit=limit,
        search=search,
        student_id=student_id,
        counselor_id=counselor_id,
        record_status=status_query,
    )


@router.post(
    "",
    response_model=CounselingRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_counseling_record_route(
    request: CounselingRecordCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> CounselingRecordResponse:
    return create_new_counseling_record(
        db=db,
        request=request,
        current_user=current_user,
    )


@router.get("/{counseling_record_id}", response_model=CounselingRecordDetailResponse)
def get_counseling_record_detail_route(
    counseling_record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> CounselingRecordDetailResponse:
    counseling_record = get_counseling_record_detail(
        db=db,
        counseling_record_id=counseling_record_id,
    )

    return CounselingRecordDetailResponse(data=counseling_record)


@router.patch("/{counseling_record_id}", response_model=CounselingRecordResponse)
def update_counseling_record_route(
    counseling_record_id: int,
    request: CounselingRecordUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> CounselingRecordResponse:
    return update_existing_counseling_record(
        db=db,
        counseling_record_id=counseling_record_id,
        request=request,
    )


@router.delete("/{counseling_record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_counseling_record_route(
    counseling_record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ADMIN, COUNSELOR)),
) -> None:
    delete_existing_counseling_record(
        db=db,
        counseling_record_id=counseling_record_id,
    )