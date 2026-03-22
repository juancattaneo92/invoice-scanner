"""
Invoice Scanner: SQLAlchemy ORM models for database
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.storage_service.database import Base

class Invoice(Base):
    """Invoice table"""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String(255), nullable=False)
    invoice_number = Column(String(100), nullable=True, unique=True)
    date = Column(String(20), nullable=False)
    total = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=True)
    tax = Column(Float, nullable=True)
    status = Column(String(50), default="completed", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    line_items = relationship("LineItem", back_populates="invoice", cascade="all, delete-orphan")

class LineItem(Base):
    """Line items in invoice"""
    __tablename__ = "line_items"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    description = Column(String(500), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="line_items")