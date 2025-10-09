# app/models/orders.py
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    details = Column(Text)

    # Relaciones
    user = relationship("User", back_populates="orders")
    company = relationship("Company", back_populates="orders")
