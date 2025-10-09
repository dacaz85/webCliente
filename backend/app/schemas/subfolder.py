# app/schemas/subfolder.py
from pydantic import BaseModel
from typing import Optional

class SubfolderBase(BaseModel):
    company_id: int
    name: str
    path: str

class SubfolderCreate(SubfolderBase):
    pass

class SubfolderUpdate(BaseModel):
    name: Optional[str]
    path: Optional[str]

class SubfolderResponse(SubfolderBase):
    id: int

    class Config:
        orm_mode = True
