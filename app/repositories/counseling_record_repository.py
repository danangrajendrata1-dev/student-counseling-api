from uuid import UUID
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.counseling_record_model import CounselingRecord


def get_counseling_record_by_id(
    db: Session,
    counseling_record_id: int,
) -> CounselingRecord | None:
    statement = select(CounselingRecord).where(
        CounselingRecord.id == counseling_record_id
    )

    return db.execute(statement).scalar_one_or_none()


def get_counseling_records(
    db: Session,
    *,
    offset: int,
    limit: int,
    search: str | None = None,
    student_id: UUID | None = None,
    counselor_id: UUID | None = None,
    status: str | None = None,
) -> tuple[list[CounselingRecord], int]:
    statement = select(CounselingRecord)
    count_statement = select(func.count(CounselingRecord.id))

    statement, count_statement = _apply_counseling_record_filters(
        statement=statement,
        count_statement=count_statement,
        search=search,
        student_id=student_id,
        counselor_id=counselor_id,
        status=status,
    )

    total = db.execute(count_statement).scalar_one()

    records = db.execute(
        statement
        .order_by(CounselingRecord.counseling_date.desc(), CounselingRecord.id.desc())
        .offset(offset)
        .limit(limit)
    ).scalars().all()

    return list(records), total


def create_counseling_record(
    db: Session,
    counseling_record: CounselingRecord,
) -> CounselingRecord:
    db.add(counseling_record)
    db.commit()
    db.refresh(counseling_record)

    return counseling_record


def update_counseling_record(
    db: Session,
    counseling_record: CounselingRecord,
    update_data: dict,
) -> CounselingRecord:
    for field, value in update_data.items():
        setattr(counseling_record, field, value)

    db.commit()
    db.refresh(counseling_record)

    return counseling_record


def delete_counseling_record(
    db: Session,
    counseling_record: CounselingRecord,
) -> None:
    db.delete(counseling_record)
    db.commit()


def _apply_counseling_record_filters(
    *,
    statement: Select,
    count_statement: Select,
    search: str | None,
    student_id: UUID | None,
    counselor_id: UUID | None,
    status: str | None,
) -> tuple[Select, Select]:
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            CounselingRecord.topic.ilike(search_pattern)
        )
        count_statement = count_statement.where(
            CounselingRecord.topic.ilike(search_pattern)
        )

    if student_id:
        statement = statement.where(CounselingRecord.student_id == student_id)
        count_statement = count_statement.where(CounselingRecord.student_id == student_id)

    if counselor_id:
        statement = statement.where(CounselingRecord.counselor_id == counselor_id)
        count_statement = count_statement.where(
            CounselingRecord.counselor_id == counselor_id
        )

    if status:
        statement = statement.where(CounselingRecord.status == status)
        count_statement = count_statement.where(CounselingRecord.status == status)

    return statement, count_statement