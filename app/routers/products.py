from fastapi import APIRouter, HTTPException
from app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    return product_service.create_product(product)

@router.get("/", response_model=list[ProductResponse])
def get_products():
    return product_service.get_products()
        
@router.get("/{product_id}",
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
            

@router.put("/{product_id}")
def update_product(product_id: int, updated_product: ProductCreate):
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


@router.delete("/{product_id}")
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