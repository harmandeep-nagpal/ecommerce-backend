from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
        description="The name of the product"
    )

    price: float = Field(
        gt=0,
        description="The price of the product"
    )

    stock: int = Field(
        ge=0,
        description="Available units in the inventory"
    )


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    price: float | None = Field(
        default=None,
        gt=0
    )

    stock: int | None = Field(
        default=None,
        ge=0
    )


class ProductResponse(BaseModel):
    id: int = Field(gt=0)
    name: str
    price: float
    stock: int

    model_config = {
        "from_attributes": True
    }

class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    page: int
    limit: int
    total: int
    pages: int