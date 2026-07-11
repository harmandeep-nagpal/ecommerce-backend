from fastapi import HTTPException
from app.schemas import ProductCreate, ProductResponse

products: list[ProductResponse] = []
next_product_id = 1


def create_product(product: ProductCreate):
    global next_product_id

    product_dict = product.model_dump()

    product_response = ProductResponse(
        id=next_product_id,
        **product_dict
    )

    products.append(product_response)

    next_product_id += 1

    return product_response

def get_products(limit: int = 10, skip: int = 0):
    return products[skip : skip + limit]

def update_product(product_id: int, updated_product: ProductCreate):
    for product in products:
        if product.id == product_id:
            product.name = updated_product.name
            product.price = updated_product.price
            product.stock = updated_product.stock
            return product
    raise HTTPException(
        status_code=404,
        detail=f"Product with ID {product_id} not found"
    )

def delete_product(product_id: int):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return product
    raise HTTPException(
    status_code=404,
    detail=f"Product with ID {product_id} not found"
)