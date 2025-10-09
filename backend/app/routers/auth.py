# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

from app.database import get_db
from app.models import User
from app.utils.security import verify_password
from app.utils.jwt import create_access_token, create_refresh_token
from app.schemas.token import Token  # Asegúrate de tener este schema

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Filtramos por email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.status:
        raise HTTPException(status_code=403, detail="User not active")
    
    # Actualizamos last_login
    user.last_login = datetime.utcnow()
    db.commit()

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
