# app/models/subfolders.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Subfolder(Base):
    __tablename__ = "subfolders"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)

    # Relaciones
    company = relationship("Company", back_populates="subfolders")
    permissions = relationship("Permission", back_populates="subfolder", cascade="all, delete-orphan")
