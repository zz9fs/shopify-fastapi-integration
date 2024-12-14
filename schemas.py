# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Customer Schemas
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerSchema(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Order Schemas
class OrderBase(BaseModel):
    order_number: str
    customer_id: Optional[int] = None
    total_amount: float
    status: str

class OrderCreate(OrderBase):
    pass

class OrderSchema(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Existing Customer and Order Schemas...

# Product Schemas
class Product(BaseModel):
    id: int
    title: str
    body_html: str
    vendor: str
    product_type: str
    created_at: datetime
    handle: str
    updated_at: datetime
    published_at: datetime
    template_suffix: Optional[str]
    tags: str

    class Config:
        orm_mode = True

class ProductSchema(BaseModel):
    products: List[Product]

