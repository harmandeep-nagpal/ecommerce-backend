from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import UserCreate, UserResponse, UserLogin
from app.services import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_user(user, db)

@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return user_service.login_user(
        user.email,
        user.password,
        db
    )