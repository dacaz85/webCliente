# app/routers/permissions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List

from app.database import get_db
from app.models import Permission, User, Company, Subfolder
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from app.dependencies import has_role, get_current_user

router = APIRouter(prefix="/permissions", tags=["permissions"])

# -------------------------
# LIST ALL PERMISSIONS (admin)
# -------------------------
@router.get("/", response_model=List[PermissionResponse])
def list_permissions(db: Session = Depends(get_db), admin: User = Depends(has_role("admin"))):
    return db.query(Permission).all()

# -------------------------
# LIST PERMISSIONS BY USER
# -------------------------
@router.get("/user/{user_id}", response_model=List[PermissionResponse])
def list_permissions_by_user(user_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    if current.role != "admin" and current.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db.query(Permission).filter(Permission.user_id == user_id).all()

# -------------------------
# LIST PERMISSIONS BY SUBFOLDER
# -------------------------
@router.get("/subfolder/{subfolder_id}", response_model=List[PermissionResponse])
def list_permissions_by_subfolder(subfolder_id: int, db: Session = Depends(get_db), admin: User = Depends(has_role("admin"))):
    return db.query(Permission).filter(Permission.subfolder_id == subfolder_id).all()

# -------------------------
# CREATE PERMISSION
# -------------------------
@router.post("/", response_model=PermissionResponse)
def create_permission(permission_in: PermissionCreate, db: Session = Depends(get_db), admin: User = Depends(has_role("admin"))):
    # Evitar duplicados
    existing = db.query(Permission).filter(
        and_(
            Permission.user_id == permission_in.user_id,
            Permission.company_id == permission_in.company_id,
            Permission.subfolder_id == permission_in.subfolder_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")

    permission = Permission(
        user_id=permission_in.user_id,
        company_id=permission_in.company_id,
        subfolder_id=permission_in.subfolder_id,
        can_read=permission_in.can_read,
        can_write=permission_in.can_write
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

# -------------------------
# UPDATE PERMISSION
# -------------------------
@router.patch("/{permission_id}", response_model=PermissionResponse)
def update_permission(permission_id: int, permission_update: PermissionUpdate, db: Session = Depends(get_db), admin: User = Depends(has_role("admin"))):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    for key, value in permission_update.dict(exclude_unset=True).items():
        setattr(permission, key, value)
    db.commit()
    db.refresh(permission)
    return permission

# -------------------------
# DELETE PERMISSION
# -------------------------
@router.delete("/{permission_id}", status_code=204)
def delete_permission(permission_id: int, db: Session = Depends(get_db), admin: User = Depends(has_role("admin"))):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(permission)
    db.commit()
    return
