# app/schemas/order.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    company_id: int
    details: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    details: Optional[str]

class OrderResponse(OrderBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
