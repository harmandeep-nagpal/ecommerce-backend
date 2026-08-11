from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem


def get_cart_by_user_id(
    user_id: int,
    db: Session
):
    return (
        db.query(Cart)
        .filter(Cart.user_id == user_id)
        .first()
    )


def create_cart(
    user_id: int,
    db: Session
):
    cart = Cart(
        user_id=user_id
    )

    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart


def get_cart_item(
    cart_id: int,
    product_id: int,
    db: Session
):
    return (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id
        )
        .first()
    )


def create_cart_item(
    cart_item: CartItem,
    db: Session
):
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


def update_cart_item(
    cart_item: CartItem,
    db: Session
):
    db.commit()
    db.refresh(cart_item)

    return cart_item


def delete_cart_item(
    cart_item: CartItem,
    db: Session
):
    db.delete(cart_item)
    db.commit()

    return cart_item