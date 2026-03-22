"""
Invoice Scanner: Storage Service - FastAPI application
Handles database operations for invoices
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.shared.logger import logger
from src.shared.exceptions import DatabaseException
from src.shared.models import InvoiceCreate
from src.storage_service.database import get_db, init_db
from src.storage_service.queries import invoice_queries
from src.storage_service.config import SERVICE_PORT, SERVICE_NAME, SERVICE_TITLE, SERVICE_DESCRIPTION, SERVICE_API_VERSION

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info(f"{SERVICE_NAME} starting on port {SERVICE_PORT}")
    init_db()
    yield
    # Shutdown
    logger.info(f"{SERVICE_NAME} shutting down")

# Create FastAPI app
app = FastAPI(
    title=SERVICE_TITLE,
    description=SERVICE_DESCRIPTION,
    version=SERVICE_API_VERSION,
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": SERVICE_NAME
    }

@app.post("/save")
async def save_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    """
    Save extracted invoice data to database
    
    Args:
        data: Invoice data to save
        db: Database session
        
    Returns:
        Created invoice with ID
    """
    try:
        logger.info(f"Saving invoice: {data.vendor}")
        
        invoice = invoice_queries.create_invoice(db, data)
        
        return JSONResponse({
            "status": "success",
            "invoice_id": invoice.id,
            "vendor": invoice.vendor,
            "total": invoice.total
        })
    
    except DatabaseException as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error in save: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/invoice/{invoice_id}")
async def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Get invoice by ID
    
    Args:
        invoice_id: Invoice ID
        db: Database session
        
    Returns:
        Invoice data
    """
    try:
        invoice = invoice_queries.get_invoice(db, invoice_id)
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        return JSONResponse({
            "status": "success",
            "id": invoice.id,
            "vendor": invoice.vendor,
            "date": invoice.date,
            "total": invoice.total,
            "subtotal": invoice.subtotal,
            "tax": invoice.tax,
            "status": invoice.status
        })
    
    except DatabaseException as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error in get: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/invoices")
async def list_invoices(db: Session = Depends(get_db)):
    """
    List all invoices
    
    Args:
        db: Database session
        
    Returns:
        List of invoices
    """
    try:
        invoices = invoice_queries.get_all_invoices(db)
        
        return JSONResponse({
            "status": "success",
            "count": len(invoices),
            "invoices": [
                {
                    "id": inv.id,
                    "vendor": inv.vendor,
                    "date": inv.date,
                    "total": inv.total,
                    "status": inv.status
                }
                for inv in invoices
            ]
        })
    
    except Exception as e:
        logger.error(f"Error listing invoices: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# To run the service, use the command at config.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=SERVICE_PORT,
        reload=True
    )