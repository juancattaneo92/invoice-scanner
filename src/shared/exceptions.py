"""
Invoice Scanner: Custom exceptions for the application
This file defines custom error classes specific to this application.
Instead of generic Python errors, we will get more meaningful errors.
"""

class InvoiceScannerException(Exception):
    """Base exception for invoice scanner"""
    pass

class OCRException(InvoiceScannerException):
    """Raised when OCR processing fails"""
    pass

class LLMException(InvoiceScannerException):
    """Raised when LLM processing fails"""
    pass

class ValidationException(InvoiceScannerException):
    """Raised when data validation fails"""
    pass

class DatabaseException(InvoiceScannerException):
    """Raised when database operations fail"""
    pass

class ServiceUnavailableException(InvoiceScannerException):
    """Raised when a service is unavailable"""
    pass

__all__ = [
    "InvoiceScannerException",
    "OCRException",
    "LLMException",
    "ValidationException",
    "DatabaseException",
    "ServiceUnavailableException",
]