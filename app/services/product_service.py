from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate

def get_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

def create_product(product: ProductCreate, db: Session):
    db_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product(product_id: int, db: Session):
    return get_product_by_id(product_id, db)


def update_product(product_id: int, updated_product: ProductCreate, db: Session):
    product = get_product_by_id(product_id, db)
    product.name = updated_product.name
    product.price = updated_product.price
    product.stock = updated_product.stock

    db.commit()
    db.refresh(product)

    return product


def delete_product(product_id: int, db: Session):
    product = get_product_by_id(product_id, db)

    db.delete(product)
    db.commit()

    return product

def patch_product(product_id: int, updated_product: ProductUpdate, db: Session):
    product = get_product_by_id(product_id, db)

    update_data = updated_product.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product