# app/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import Order, User, Company
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.dependencies import has_role, get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

# -------------------------
# LIST ALL ORDERS (admin)
# -------------------------
@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db), admin: User = Depends(has_role("admin"))):
    return db.query(Order).all()

# -------------------------
# LIST ORDERS BY USER
# -------------------------
@router.get("/user/{user_id}", response_model=List[OrderResponse])
def list_orders_by_user(user_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    if current.role != "admin" and current.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db.query(Order).filter(Order.user_id == user_id).all()

# -------------------------
# LIST ORDERS BY COMPANY
# -------------------------
@router.get("/company/{company_id}", response_model=List[OrderResponse])
def list_orders_by_company(company_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    # Admin puede ver todos, cliente solo si tiene permisos
    if current.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view orders by company")
    return db.query(Order).filter(Order.company_id == company_id).all()

# -------------------------
# GET ORDER BY ID
# -------------------------
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current.role != "admin" and current.id != order.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return order

# -------------------------
# CREATE ORDER
# -------------------------
@router.post("/", response_model=OrderResponse)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    # El usuario que crea el pedido siempre es current_user
    order = Order(
        user_id=current.id,
        company_id=order_in.company_id,
        details=order_in.details,
        created_at=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

# -------------------------
# UPDATE ORDER
# -------------------------
@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current.role != "admin" and current.id != order.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order

# -------------------------
# DELETE ORDER
# -------------------------
@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current.role != "admin" and current.id != order.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(order)
    db.commit()
    return
