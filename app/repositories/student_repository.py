import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.student_model import Student


def get_student_by_id(db: Session, student_id: uuid.UUID) -> Student | None:
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_nis(db: Session, nis: str) -> Student | None:
    return db.query(Student).filter(Student.nis == nis).first()


def get_students(
    db: Session,
    *,
    search: str | None,
    class_name: str | None,
    major: str | None,
    academic_year: str | None,
    status: str | None,
    offset: int,
    limit: int,
) -> tuple[list[Student], int]:
    query = db.query(Student)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Student.name.ilike(search_pattern),
                Student.nis.ilike(search_pattern),
            )
        )

    if class_name:
        query = query.filter(Student.class_name == class_name)

    if major:
        query = query.filter(Student.major == major)

    if academic_year:
        query = query.filter(Student.academic_year == academic_year)

    if status:
        query = query.filter(Student.status == status)

    total = query.count()

    students = (
        query
        .order_by(Student.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return students, total


def create_student(db: Session, payload: dict) -> Student:
    student = Student(**payload)

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def update_student(db: Session, student: Student, payload: dict) -> Student:
    for field, value in payload.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student: Student) -> None:
    db.delete(student)
    db.commit()