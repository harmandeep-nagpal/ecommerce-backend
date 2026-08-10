from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
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

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user = Depends(get_current_user)
):
    return current_user