from fastapi import FastAPI
from app.routers import products
from app.db.database import Base, engine
from app.models.product import Product

Base.metadata.create_all(bind=engine)

APP_NAME = "E-commerce Backend"

APP_DESCRIPTION = "Production-ready e-commerce backend built with FastAPI."

APP_VERSION = "1.0.0"

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

app.include_router(products.router)

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
