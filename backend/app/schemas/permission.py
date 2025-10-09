# app/schemas/permission.py
from pydantic import BaseModel
from typing import Optional

class PermissionBase(BaseModel):
    user_id: int
    company_id: int
    subfolder_id: int
    can_read: Optional[bool] = True
    can_write: Optional[bool] = False

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    can_read: Optional[bool]
    can_write: Optional[bool]

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        orm_mode = True
