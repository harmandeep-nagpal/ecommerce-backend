from fastapi import FastAPI, HTTPException
from app.schemas import Product, ProductResponse

APP_NAME = "E-commerce Backend"

APP_DESCRIPTION = "Production-ready e-commerce backend built with FastAPI."

APP_VERSION = "1.0.0"

products = []
next_product_id = 1

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

@app.get("/")
def home():
    return {
        "message" : "Welcome to the E-Commerce Backend API"
    }

@app.get("/health")
def health():
    return {
        "status" : "healthy"
    }

@app.get("/version")
def get_version():
    return {
        "version" : APP_VERSION
    }

@app.post("/products")
def create_product(product: Product):
    global next_product_id

    product_dict = product.model_dump()      # Convert Pydantic model to dictionary
    product_dict["id"] = next_product_id     # Assign ID

    products.append(product_dict)

    next_product_id += 1                     # Increment for next product

    return {
        "message": "Product created successfully",
        "product": product_dict
    }

@app.get("/products")
def get_products(limit: int = 10, skip: int = 0):
    return {
        "message": "Fetch all products",
        "products" : products[skip : skip + limit],
        "limit": limit,
        "skip": skip
        }
        
@app.get("/products/{product_id}",
        response_model=ProductResponse) # It tells FastAPI: "Whatever this function returns must match the ProductResponse schema."
def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {
                "product": product,
                "message": "Product found"
            }
    raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
            

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for product in products:
        if product["id"] == product_id:
            product["name"] = updated_product.name
            product["price"] = updated_product.price
            product["stock"] = updated_product.stock
            return {
                "product" : product,
                "message" : f"The updated producct with the product id {product_id} is"
            } 
    raise HTTPException(
        status_code=404,
        detail=f"Product with ID {product_id} not found"
    )


@app.patch("/products/{product_id}")
def patch_product(product_id: int):
    return {
        "product_id": product_id,
        "message": "Product partially updated"
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {
                "product_id": product_id,
                "message": "Product deleted"
            }
    raise HTTPException(
        status_code=404,
        detail= f"The product with ID = {product_id} can't be found"
    )