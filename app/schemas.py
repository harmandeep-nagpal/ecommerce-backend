from pydantic import BaseModel 

class Product(BaseModel): # BaseModel is the class provided by Pydantic that enables automatic validation and parsing.
    name: str
    price: float
    stock: int