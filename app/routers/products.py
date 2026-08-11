from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal
from app.core.security import get_current_admin
from app.db.database import get_db
from app.schemas import ProductCreate, ProductResponse, ProductUpdate, ProductListResponse
from app.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# ==========================================================
# Product CRUD APIs
# ==========================================================


# ADMIN ONLY
@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return product_service.create_product(product, db)


# PUBLIC / AUTHENTICATED USERS CAN VIEW
@router.get("/", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, min_length=1),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    sort_by: Literal["id", "name", "price"] = Query("id"),
    order: Literal["asc", "desc"] = Query("asc"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    return product_service.get_all_products(
        db,
        skip,
        limit,
        search,
        min_price,
        max_price,
        sort_by,
        order
    )

# PUBLIC / AUTHENTICATED USERS CAN VIEW
@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    return product_service.get_product(product_id, db)


# ADMIN ONLY
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return product_service.update_product(
        product_id,
        updated_product,
        db
    )


# ADMIN ONLY
@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return product_service.delete_product(
        product_id,
        db
    )


# ADMIN ONLY
@router.patch("/{product_id}", response_model=ProductResponse)
def patch_product(
    product_id: int,
    updated_product: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return product_service.patch_product(
        product_id,
        updated_product,
        db
    )