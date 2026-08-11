from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem

from app.repositories import (
    order_repository,
    cart_repository,
    product_repository
)


def checkout(
    user_id: int,
    db: Session
):
    # Get user's cart
    cart = cart_repository.get_cart_by_user_id(
        user_id,
        db
    )

    if cart is None or not cart.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    # Check stock and calculate total
    total_amount = 0

    for cart_item in cart.items:

        product = product_repository.get_product_by_id(
            cart_item.product_id,
            db
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product {cart_item.product_id} not found"
            )

        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        total_amount += (
            product.price * cart_item.quantity
        )

    # Create order
    order = Order(
        user_id=user_id,
        status="pending",
        total_amount=total_amount
    )

    order_repository.create_order(
        order,
        db
    )

    # Create order items and reduce stock
    for cart_item in cart.items:

        product = product_repository.get_product_by_id(
            cart_item.product_id,
            db
        )

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            unit_price=product.price
        )

        order_repository.create_order_item(
            order_item,
            db
        )

        product.stock -= cart_item.quantity

    # Remove cart items
    for cart_item in list(cart.items):
        db.delete(cart_item)

    # Commit the complete transaction
    db.commit()

    db.refresh(order)

    return order

def get_user_orders(
    user_id: int,
    db: Session
):
    return order_repository.get_orders_by_user_id(
        user_id,
        db
    )


def get_user_order(
    user_id: int,
    order_id: int,
    db: Session
):
    order = order_repository.get_order_by_id(
        order_id,
        db
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access this order"
        )

    return order

def update_order_status(
    order_id: int,
    status: str,
    db: Session
):
    order = order_repository.get_order_by_id(
        order_id,
        db
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    allowed_statuses = {
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled"
    }

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    order.status = status

    return order_repository.update_order(
        order,
        db
    )