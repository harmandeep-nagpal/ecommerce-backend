from fastapi import FastAPI
from app.schemas import Product

APP_NAME = "E-commerce Backend"

APP_DESCRIPTION = "Production-ready e-commerce backend built with FastAPI."

APP_VERSION = "1.0.0"

products = []

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
    products.append(product)
    return {
        "message": "Product created successfully",
        "product": product
    }

@app.get("/products")
def get_products(limit: int = 10, skip: int = 0):
    return {
        "message": "Fetch all products",
        "products" : products[skip : skip + limit],
        "limit": limit,
        "skip": skip
        }


@app.put("/products/{product_id}")
def update_product(product_id: int):
    return {
        "product_id": product_id,
        "message": "Product updated"
    }


@app.patch("/products/{product_id}")
def patch_product(product_id: int):
    return {
        "product_id": product_id,
        "message": "Product partially updated"
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {
        "product_id": product_id,
        "message": "Product deleted"
    }