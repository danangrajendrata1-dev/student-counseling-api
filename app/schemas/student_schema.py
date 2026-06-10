import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class StudentCreateRequest(BaseModel):
    nis: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=2, max_length=150)
    gender: str = Field(min_length=1, max_length=20)
    class_name: str = Field(min_length=1, max_length=50)
    major: str | None = Field(default=None, max_length=100)
    academic_year: str = Field(min_length=4, max_length=20)
    phone: str | None = Field(default=None, max_length=30)
    address: str | None = None
    status: str = Field(default="active")


class StudentUpdateRequest(BaseModel):
    nis: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=2, max_length=150)
    gender: str | None = Field(default=None, min_length=1, max_length=20)
    class_name: str | None = Field(default=None, min_length=1, max_length=50)
    major: str | None = Field(default=None, max_length=100)
    academic_year: str | None = Field(default=None, min_length=4, max_length=20)
    phone: str | None = Field(default=None, max_length=30)
    address: str | None = None
    status: str | None = Field(default=None)


class StudentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    nis: str
    name: str
    gender: str
    class_name: str
    major: str | None
    academic_year: str
    phone: str | None
    address: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class StudentListResponse(BaseModel):
    message: str
    data: list[StudentResponse]
    pagination: dict


class StudentDetailResponse(BaseModel):
    message: str
    data: StudentResponse