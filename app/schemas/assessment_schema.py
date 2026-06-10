from uuid import UUID
from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from app.constants.assessment_type import ALLOWED_ASSESSMENT_TYPES


class AssessmentCreateRequest(BaseModel):
    student_id: UUID 
    assessment_type: str = Field(..., min_length=3, max_length=50)
    assessment_date: date
    score: int | None = Field(default=None, ge=0)
    result: str = Field(..., min_length=3, max_length=150)
    notes: str | None = None

    @field_validator("assessment_type")
    @classmethod
    def validate_assessment_type(cls, value: str) -> str:
        if value not in ALLOWED_ASSESSMENT_TYPES:
            raise ValueError(
                f"Assessment type must be one of: {', '.join(ALLOWED_ASSESSMENT_TYPES)}"
            )
        return value


class AssessmentUpdateRequest(BaseModel):
    assessment_type: str | None = Field(default=None, min_length=3, max_length=50)
    assessment_date: date | None = None
    score: int | None = Field(default=None, ge=0)
    result: str | None = Field(default=None, min_length=3, max_length=150)
    notes: str | None = None

    @field_validator("assessment_type")
    @classmethod
    def validate_assessment_type(cls, value: str | None) -> str | None:
        if value is not None and value not in ALLOWED_ASSESSMENT_TYPES:
            raise ValueError(
                f"Assessment type must be one of: {', '.join(ALLOWED_ASSESSMENT_TYPES)}"
            )
        return value


class AssessmentResponse(BaseModel):
    id: int
    student_id: UUID
    created_by: UUID
    assessment_type: str
    assessment_date: date
    score: int | None
    result: str
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class AssessmentListResponse(BaseModel):
    data: list[AssessmentResponse]
    meta: dict


class AssessmentDetailResponse(BaseModel):
    data: AssessmentResponse