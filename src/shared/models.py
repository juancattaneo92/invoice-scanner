"""
Invoice Parser: Shared data models used across services.
This file defines data validation schemas using Pydantic. 
These are the data types the app accepts and returns.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InvoiceCreate(BaseModel):
    """Request model for creating invoice"""
    vendor: str
    date: str
    total: float
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    items: Optional[List[dict]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "vendor": "Test Vendor Co.",
                "date": "2026-01-01",
                "total": 100.00,
                "subtotal": 90.00,
                "tax": 10.00,
                "items": [
                    {"description": "Item 1", "quantity": 1, "unit_price": 90.00}
                ]
            }
        }

class InvoiceResponse(BaseModel):
    """Response model for invoice data"""
    id: int
    vendor: str
    date: str
    total: float
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class LineItemResponse(BaseModel):
    """Line item in invoice"""
    id: int
    description: str
    quantity: int
    unit_price: float
    line_total: float
    
    class Config:
        from_attributes = True

class ExtractionResponse(BaseModel):
    """Full extraction with items"""
    invoice: InvoiceResponse
    items: List[LineItemResponse]

class UploadResponse(BaseModel):
    """Response after upload"""
    invoice_id: int
    status: str
    message: str

class StatusResponse(BaseModel):
    """Status check response"""
    invoice_id: int
    status: str
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    details: Optional[str] = None

__all__ = [
    "InvoiceCreate",
    "InvoiceResponse",
    "LineItemResponse",
    "ExtractionResponse",
    "UploadResponse",
    "StatusResponse",
    "ErrorResponse",
]