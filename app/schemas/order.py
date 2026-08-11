from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    model_config = {
        "from_attributes": True
    }


class OrderResponse(BaseModel):
    id: int
    status: str
    total_amount: float
    items: list[OrderItemResponse]

    model_config = {
        "from_attributes": True
    }

class OrderStatusUpdate(BaseModel):
    status: str