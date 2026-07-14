from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)
# ================================

# Dependency Injection Practice
# Temporary learning examples
# Will be removed before production implementation

def get_name():
    return "Harry"
def greet_user(name: str = Depends(get_name)):
    return f"Hello {name}"
@router.get("/chain")
def dependency_chain(message: str = Depends(greet_user)):
    return {"message": message}

def get_msg(name : str):
    return f"Hello, {name}"

@router.get("/hello")
def hello(message: str = Depends(get_msg)):
    return {"message": message}


def verify_api_key(api_key : str):
    if api_key == "secret123":
        return
    else:
        raise HTTPException(
            status_code=401,
            detail="Wrong Api key"
        )
# ================================

@router.get("/protected")
def protected(_: None = Depends(verify_api_key)):
    return {
    "message": "You are authorized"
} 

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return product_service.create_product(product, db)

@router.get("/", response_model=list[ProductResponse])
def get_products(limit: int = 10, skip: int = 0):
    return product_service.get_products(limit, skip)
              
@router.get("/{product_id}", response_model=ProductResponse) # It tells FastAPI: "Whatever this function returns must match the ProductResponse schema."
def get_product_by_id(product_id: int):
    return product_service.get_product_by_id(product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated_product: ProductCreate):
    return product_service.update_product(product_id, updated_product)

@router.delete("/{product_id}",response_model=ProductResponse)
def delete_product(product_id: int):
    return product_service.delete_product(product_id)

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, update: ProductUpdate):
        for product in products:
            if product["id"] == product_id:   
                update_data = update.model_dump(exclude_unset=True)
                for key, value in update_data.items():# .items() is predefined py dictionary method.It returns every key-value pair.
                    product[key] = value
                return {
                    "product" : product,
                    "message" : "The product was updated succesfully"
                }
        raise HTTPException(
            status_code=404,
            detail=f"The product with ID {product_id} can't be found"
        )


