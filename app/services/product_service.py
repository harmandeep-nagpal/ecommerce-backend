from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories import product_repository
import math
from app.models.product import Product
from app.schemas import ProductCreate, ProductUpdate

def create_product(product: ProductCreate, db: Session):
    db_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    return product_repository.create_product(db_product,db)

def get_all_products(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort_by: str = "id",
    order: str = "asc"
):
    if (
    min_price is not None
    and max_price is not None
    and min_price > max_price
):
        raise HTTPException(
        status_code=400,
        detail="min_price cannot be greater than max_price"
    )
    products, total = product_repository.get_all_products(
        db,
        skip,
        limit,
        search,
        min_price,
        max_price,
        sort_by,
        order
    )

    page = (skip // limit) + 1
    pages = math.ceil(total / limit)

    return {
        "items": products,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }


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