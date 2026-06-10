from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.constants.roles import ALLOWED_ROLES
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import create_user, get_user_by_email
from app.schemas.auth_schema import LoginRequest, RegisterRequest


def register_user(db: Session, payload: RegisterRequest):
    existing_user = get_user_by_email(db, payload.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    if payload.role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role",
        )

    hashed = hash_password(payload.password)

    return create_user(
        db,
        name=payload.name,
        email=payload.email,
        hashed_password=hashed,
        role=payload.role,
    )


def login_user(db: Session, payload: LoginRequest) -> str:
    user = get_user_by_email(db, payload.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    password_valid = verify_password(payload.password, user.hashed_password)

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return create_access_token(str(user.id))