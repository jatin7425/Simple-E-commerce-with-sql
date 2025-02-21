from pydantic import BaseModel
from typing import List

# Products 
class ProductBase(BaseModel):
    name: str
    description: str
    price: int

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Correct for Pydantic v2



# order
class OrderBase(BaseModel):
    user_id: int

class OrderCreate(BaseModel):
    product_ids: List[int]  # List of product IDs being ordered

class OrderUpdate(BaseModel):
    status: str

class OrderResponse(OrderBase):
    id: int
    user_id: int
    products: List[ProductResponse]

    class Config:
        from_attributes = True  # Ensures compatibility with ORM


# user
class UserCreate(BaseModel):
    username: str
    password: str

# Order schema
class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    products: List[ProductResponse]

    class Config:
        from_attributes = True

# User schema (Fix: Change `orders` to List[OrderResponse] instead of List[ProductResponse])
class UserResponse(BaseModel):
    id: int
    username: str
    orders: List[OrderResponse]  # <== FIX HERE

    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str
