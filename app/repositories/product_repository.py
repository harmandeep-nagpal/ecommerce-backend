from sqlalchemy.orm import Session

from app.models.product import Product

def get_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()

    return product

def create_product(db_product: Product, db: Session):

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def get_all_products(db: Session):
    return db.query(Product).all()

def update_product(product: Product, db: Session):
    db.commit()
    db.refresh(product)

    return product

def delete_product(product: Product, db: Session):
    db.delete(product)
    db.commit()
    
    return product