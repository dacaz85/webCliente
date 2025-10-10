# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models import User
from app.utils.security import verify_password
from app.utils.jwt import create_access_token, create_refresh_token
from app.schemas.token import Token
from app.schemas.user import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Filtramos por email
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.status:
        raise HTTPException(status_code=403, detail="User not active")
    
    # Actualizamos last_login
    user.last_login = datetime.utcnow()
    db.commit()

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
