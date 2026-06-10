from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user_model import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    *,
    name: str,
    email: str,
    hashed_password: str,
    role: str,
) -> User:
    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user