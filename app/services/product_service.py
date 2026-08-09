from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories import product_repository

from app.models.product import Product
from app.schemas import ProductCreate, ProductUpdate

def create_product(product: ProductCreate, db: Session):
    db_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    return product_repository.create_product(db_product,db)


def get_all_products(db: Session):
    return product_repository.get_all_products(db)


def get_product(product_id: int, db: Session):
    product = product_repository.get_product_by_id(product_id, db)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


def update_product(product_id: int, updated_product: ProductCreate, db: Session):
    product = product_repository.get_product_by_id(
        product_id,
        db
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = updated_product.name
    product.price = updated_product.price
    product.stock = updated_product.stock

    return product_repository.update_product(product, db)


def delete_product(product_id: int, db: Session):
    product = product_repository.get_product_by_id(
        product_id,
        db
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product_repository.delete_product(product, db)

def patch_product(product_id: int, updated_product: ProductUpdate, db: Session):
    product = product_repository.get_product_by_id(
        product_id,
        db
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found")

    update_data = updated_product.model_dump(
        exclude_unset=True
    )
    
    for key, value in update_data.items():
        setattr(product, key, value)

    return product_repository.update_product(
        product,
        db
    )