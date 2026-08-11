from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user, get_current_admin
from app.db.database import get_db
from app.schemas import OrderResponse, OrderStatusUpdate
from app.services import order_service


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/checkout",
    response_model=OrderResponse
)
def checkout(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return order_service.checkout(
        current_user.id,
        db
    )

@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_my_orders(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return order_service.get_user_orders(
        current_user.id,
        db
    )

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_my_order(
    order_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return order_service.get_user_order(
        current_user.id,
        order_id,
        db
    )

@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return order_service.update_order_status(
        order_id,
        status_update.status,
        db
    )