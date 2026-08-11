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
    query = db.query(Product)

    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    # Sorting
    if sort_by == "price":
        sort_column = Product.price
    elif sort_by == "name":
        sort_column = Product.name
    else:
        sort_column = Product.id

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    products = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    total = query.count()

    return products, total

def update_product(product: Product, db: Session):
    db.commit()
    db.refresh(product)

    return product

def delete_product(product: Product, db: Session):
    db.delete(product)
    db.commit()
    
    return product