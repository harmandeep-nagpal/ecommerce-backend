from app.schemas import ProductCreate
from app.models.product import Product
from sqlalchemy.orm import Session

def create_product(
    product: ProductCreate,
    db: Session
):
    db_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product