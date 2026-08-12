from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.repositories import cart_repository
from app.repositories import product_repository


def get_or_create_cart(
    user_id: int,
    db: Session
):
    cart = cart_repository.get_cart_by_user_id(
        user_id,
        db
    )

    if cart is None:
        cart = cart_repository.create_cart(
            user_id,
            db
        )

    return cart

def get_cart_response(
    user_id: int,
    db: Session
):
    cart = get_or_create_cart(
        user_id,
        db
    )

    total = 0

    for item in cart.items:
        total += item.product.price * item.quantity

    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": cart.items,
        "total": total
    }

def add_to_cart(
    user_id: int,
    product_id: int,
    quantity: int,
    db: Session
):
    # Get or create user's cart
    cart = get_or_create_cart(
        user_id,
        db
    )

    # Check that product exists
    product = product_repository.get_product_by_id(
        product_id,
        db
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Check if product is already in cart
    cart_item = cart_repository.get_cart_item(
        cart.id,
        product_id,
        db
    )

    if cart_item is not None:
        cart_item.quantity += quantity

        return cart_repository.update_cart_item(
            cart_item,
            db
        )

    # Product isn't already in cart
    cart_item = CartItem(
        cart_id=cart.id,
        product_id=product_id,
        quantity=quantity
    )

    return cart_repository.create_cart_item(
        cart_item,
        db
    )


def update_cart_item(
    user_id: int,
    product_id: int,
    quantity: int,
    db: Session
):
    cart = cart_repository.get_cart_by_user_id(
        user_id,
        db
    )

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = cart_repository.get_cart_item(
        cart.id,
        product_id,
        db
    )

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )

    cart_item.quantity = quantity

    return cart_repository.update_cart_item(
        cart_item,
        db
    )


def remove_from_cart(
    user_id: int,
    product_id: int,
    db: Session
):
    cart = cart_repository.get_cart_by_user_id(
        user_id,
        db
    )

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = cart_repository.get_cart_item(
        cart.id,
        product_id,
        db
    )

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )

    return cart_repository.delete_cart_item(
        cart_item,
        db
    )