from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem


def create_order(
    order: Order,
    db: Session
):
    db.add(order)
    db.flush()

    return order


def create_order_item(
    order_item: OrderItem,
    db: Session
):
    db.add(order_item)

    return order_item


def get_orders_by_user_id(
    user_id: int,
    db: Session
):
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order_by_id(
    order_id: int,
    db: Session
):
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )


def update_order(
    order: Order,
    db: Session
):
    db.commit()
    db.refresh(order)

    return order