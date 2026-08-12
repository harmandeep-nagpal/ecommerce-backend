from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas import UserCreate
from app.repositories import user_repository
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
import logging

logger = logging.getLogger(__name__)

def create_user(user: UserCreate, db: Session):
    existing_user = user_repository.get_user_by_email(
        user.email,
        db
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name
    )

    return user_repository.create_user(
        db_user,
        db
    )

def login_user(email: str, password: str, db: Session):
    user = user_repository.get_user_by_email(
        email,
        db
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    access_token = create_access_token({
        "sub": str(user.id)
    })
    logger.info(
    "User login successful: user_id=%s",
    user.id
)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()