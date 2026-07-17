from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import ProductCreate, ProductResponse
from app.services import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# ==========================================================
# Dependency Injection Practice
# (Can be removed later before production)
# ==========================================================

def get_name():
    return "Harry"


def greet_user(name: str = Depends(get_name)):
    return f"Hello {name}"


@router.get("/chain")
def dependency_chain(message: str = Depends(greet_user)):
    return {"message": message}


def get_msg(name: str):
    return f"Hello, {name}"


@router.get("/hello")
def hello(message: str = Depends(get_msg)):
    return {"message": message}


def verify_api_key(api_key: str):
    if api_key != "secret123":
        raise HTTPException(
            status_code=401,
            detail="Wrong API key"
        )


@router.get("/protected")
def protected(_: None = Depends(verify_api_key)):
    return {
        "message": "You are authorized"
    }


# ==========================================================
# Product CRUD APIs
# ==========================================================

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return product_service.create_product(product, db)


@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    return product_service.get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    return product_service.get_product(product_id, db)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):
    return product_service.update_product(
        product_id,
        updated_product,
        db
    )


@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return product_service.delete_product(
        product_id,
        db
    )