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