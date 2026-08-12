from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas import CartItemCreate, CartItemUpdate, CartItemResponse, CartResponse
from app.services import cart_service


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.get("/", response_model=CartResponse)
def get_my_cart(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.get_cart_response(
        current_user.id,
        db
    )


@router.post("/items", response_model=CartItemResponse)
def add_cart_item(
    item: CartItemCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.add_to_cart(
        current_user.id,
        item.product_id,
        item.quantity,
        db
    )


@router.patch("/items/{product_id}", response_model=CartItemResponse)
def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.update_cart_item(
        current_user.id,
        product_id,
        item.quantity,
        db
    )


@router.delete("/items/{product_id}", response_model=CartItemResponse)
def remove_cart_item(
    product_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.remove_from_cart(
        current_user.id,
        product_id,
        db
    )