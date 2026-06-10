from uuid import UUID

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from app.constants.counseling_status import ALLOWED_COUNSELING_STATUSES, OPEN


class CounselingRecordCreateRequest(BaseModel):
    student_id: UUID 
    counseling_date: date
    topic: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=5)
    follow_up: str | None = None
    status: str = OPEN

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in ALLOWED_COUNSELING_STATUSES:
            raise ValueError(
                f"Status must be one of: {', '.join(ALLOWED_COUNSELING_STATUSES)}"
            )
        return value


class CounselingRecordUpdateRequest(BaseModel):
    counseling_date: date | None = None
    topic: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, min_length=5)
    follow_up: str | None = None
    status: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str | None) -> str | None:
        if value is not None and value not in ALLOWED_COUNSELING_STATUSES:
            raise ValueError(
                f"Status must be one of: {', '.join(ALLOWED_COUNSELING_STATUSES)}"
            )
        return value


class CounselingRecordResponse(BaseModel):
    id: int
    student_id: UUID
    counselor_id: UUID
    counseling_date: date
    topic: str
    description: str
    follow_up: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class CounselingRecordListResponse(BaseModel):
    data: list[CounselingRecordResponse]
    meta: dict


class CounselingRecordDetailResponse(BaseModel):
    data: CounselingRecordResponse