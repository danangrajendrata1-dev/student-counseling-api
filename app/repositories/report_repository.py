from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.assessment_model import Assessment
from app.models.counseling_record_model import CounselingRecord
from app.models.student_model import Student


def count_students(db: Session) -> int:
    statement = select(func.count(Student.id))
    return db.execute(statement).scalar_one()


def count_students_by_status(db: Session, student_status: str) -> int:
    statement = select(func.count(Student.id)).where(
        Student.status == student_status
    )
    return db.execute(statement).scalar_one()


def count_counseling_records(db: Session) -> int:
    statement = select(func.count(CounselingRecord.id))
    return db.execute(statement).scalar_one()


def count_counseling_records_by_status(
    db: Session,
    record_status: str,
) -> int:
    statement = select(func.count(CounselingRecord.id)).where(
        CounselingRecord.status == record_status
    )
    return db.execute(statement).scalar_one()


def count_assessments(db: Session) -> int:
    statement = select(func.count(Assessment.id))
    return db.execute(statement).scalar_one()


def get_counseling_records_grouped_by_status(db: Session) -> dict[str, int]:
    statement = (
        select(
            CounselingRecord.status,
            func.count(CounselingRecord.id),
        )
        .group_by(CounselingRecord.status)
    )

    rows = db.execute(statement).all()

    return {
        status: count
        for status, count in rows
    }


def get_assessments_grouped_by_type(db: Session) -> dict[str, int]:
    statement = (
        select(
            Assessment.assessment_type,
            func.count(Assessment.id),
        )
        .group_by(Assessment.assessment_type)
    )

    rows = db.execute(statement).all()

    return {
        assessment_type: count
        for assessment_type, count in rows
    }