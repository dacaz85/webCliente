# app/models/permissions.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    subfolder_id = Column(Integer, ForeignKey("subfolders.id", ondelete="CASCADE"), nullable=False)
    can_read = Column(Boolean, default=True)
    can_write = Column(Boolean, default=False)

    # Relaciones
    user = relationship("User", back_populates="permissions")
    company = relationship("Company", back_populates="permissions")
    subfolder = relationship("Subfolder", back_populates="permissions")
