# app/schemas/company.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    number: str
    name: str
    path: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    number: Optional[str]
    name: Optional[str]
    path: Optional[str]

class CompanyResponse(CompanyBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
