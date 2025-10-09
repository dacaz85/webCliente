# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import datetime
import secrets

from app.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.user import PasswordAction
from app.dependencies import has_role, get_current_user
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token

router = APIRouter(prefix="/users", tags=["users"])

# -------------------------
# CREATE USER (registro)
# -------------------------
@router.post("/", response_model=UserResponse)
def create_user(User: UserCreate, db: Session = Depends(get_db)):
    # role = cliente y status = False por defecto
    existing = db.query(User).filter(User.email == User.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        name=User.name,
        email=User.email,
        password_hash=hash_password(User.password),
        role='cliente',
        status=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# -------------------------
# LIST USERS
# -------------------------
@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(has_role("admin")),
    role: str = None,
    status: bool = None
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if status is not None:
        query = query.filter(User.status == status)
    return query.all()

# -------------------------
# GET USER
# -------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # solo admin o el propio usuario puede ver
    if current.role != "admin" and current.id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

# -------------------------
# PATCH USER (activación/admin updates)
# -------------------------
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), admin: User = Depends(has_role("admin"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# -------------------------
# DELETE USER
# -------------------------
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(has_role("admin"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return

# -------------------------
# RESET / CHANGE PASSWORD
# -------------------------
@router.post("/{user_id}/password", status_code=200)
def password_action(user_id: int, action: PasswordAction, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # RESET password -> genera y devuelve temporal (podría enviarse por email)
    if action.action == "reset":
        if current.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can reset password")
        new_pass = secrets.token_urlsafe(10)
        user.password_hash = hash_password(new_pass)
        db.commit()
        return {"new_password": new_pass}

    # CHANGE password -> usuario actual cambia su password
    elif action.action == "change":
        if current.id != user.id:
            raise HTTPException(status_code=403, detail="Cannot change another user's password")
        if not action.old_password or not action.new_password:
            raise HTTPException(status_code=400, detail="Old and new passwords required")
        if not verify_password(action.old_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Old password incorrect")
        user.password_hash = hash_password(action.new_password)
        db.commit()
        return {"detail": "Password updated successfully"}

    else:
        raise HTTPException(status_code=400, detail="Invalid action type")
