# app/models/users.py
from sqlalchemy import Column, Integer, String, Enum, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('admin', 'cliente', name="user_roles"), nullable=False, default='cliente')
    status = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    last_login = Column(TIMESTAMP, nullable=True)

    # Relaciones
    permissions = relationship("Permission", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
