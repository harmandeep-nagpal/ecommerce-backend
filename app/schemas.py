from pydantic import BaseModel, Field 

class ProductCreate(BaseModel): # BaseModel is the class provided by Pydantic that enables automatic validation and parsing.
    name: str = Field(
        min_length=3,
        max_length=100, 
        description="The name of the product")
    price: float = Field(
        gt=0, 
        description="The price of the product")
    stock: int = Field(
        ge=0,
        description = "Available units in the inventory")
    
class ProductResponse(BaseModel):  # Response model
    id : int = Field(
        gt=0
    )
    name: str = Field(
        min_length=3,
        max_length=100, 
        description="The name of the product")
    price: float = Field(
        gt=0, 
        description="The price of the product")
    stock: int = Field(
        ge=0,
        description = "Available units in the inventory")
    

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
    description: str | None = None  