# app/models/companies.py
from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(CHAR(4), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # Relaciones
    subfolders = relationship("Subfolder", back_populates="company", cascade="all, delete-orphan")
    permissions = relationship("Permission", back_populates="company", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="company", cascade="all, delete-orphan")
