from uuid import UUID
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.assessment_model import Assessment


def get_assessment_by_id(
    db: Session,
    assessment_id: int,
) -> Assessment | None:
    statement = select(Assessment).where(
        Assessment.id == assessment_id
    )

    return db.execute(statement).scalar_one_or_none()


def get_assessments(
    db: Session,
    *,
    offset: int,
    limit: int,
    search: str | None = None,
    student_id: UUID | None = None,
    created_by: UUID | None = None,
    assessment_type: str | None = None,
) -> tuple[list[Assessment], int]:
    statement = select(Assessment)
    count_statement = select(func.count(Assessment.id))

    statement, count_statement = _apply_assessment_filters(
        statement=statement,
        count_statement=count_statement,
        search=search,
        student_id=student_id,
        created_by=created_by,
        assessment_type=assessment_type,
    )

    total = db.execute(count_statement).scalar_one()

    assessments = db.execute(
        statement
        .order_by(Assessment.assessment_date.desc(), Assessment.id.desc())
        .offset(offset)
        .limit(limit)
    ).scalars().all()

    return list(assessments), total


def create_assessment(
    db: Session,
    assessment: Assessment,
) -> Assessment:
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment


def update_assessment(
    db: Session,
    assessment: Assessment,
    update_data: dict,
) -> Assessment:
    for field, value in update_data.items():
        setattr(assessment, field, value)

    db.commit()
    db.refresh(assessment)

    return assessment


def delete_assessment(
    db: Session,
    assessment: Assessment,
) -> None:
    db.delete(assessment)
    db.commit()


def _apply_assessment_filters(
    *,
    statement: Select,
    count_statement: Select,
    search: str | None,
    student_id: UUID | None,
    created_by: UUID | None,
    assessment_type: str | None,
) -> tuple[Select, Select]:
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            Assessment.result.ilike(search_pattern)
        )
        count_statement = count_statement.where(
            Assessment.result.ilike(search_pattern)
        )

    if student_id:
        statement = statement.where(Assessment.student_id == student_id)
        count_statement = count_statement.where(Assessment.student_id == student_id)

    if created_by:
        statement = statement.where(Assessment.created_by == created_by)
        count_statement = count_statement.where(Assessment.created_by == created_by)

    if assessment_type:
        statement = statement.where(Assessment.assessment_type == assessment_type)
        count_statement = count_statement.where(
            Assessment.assessment_type == assessment_type
        )

    return statement, count_statement