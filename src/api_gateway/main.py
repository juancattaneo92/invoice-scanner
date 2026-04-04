"""
Invoice Scanner: API Gateway - Main FastAPI application
Orchestrates all microservices and provides unified API
"""
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from src.shared.logger import logger
from src.shared.config import OCR_SERVICE_URL, LLM_SERVICE_URL, STORAGE_SERVICE_URL
from src.shared.exceptions import InvoiceScannerException

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("API Gateway starting on port 8000")
    logger.info(f"OCR Service: {OCR_SERVICE_URL}")
    logger.info(f"LLM Service: {LLM_SERVICE_URL}")
    logger.info(f"Storage Service: {STORAGE_SERVICE_URL}")
    yield
    # Shutdown
    logger.info("API Gateway shutting down")

# Create FastAPI app
app = FastAPI(
    title="Invoice Scanner API",
    description="Microservices-based invoice processing system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Invoice Scanner API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check all services"""
    services_status = {}
    
    # Check OCR Service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OCR_SERVICE_URL}/health", timeout=2.0)
            services_status["ocr"] = response.status_code == 200
    except:
        services_status["ocr"] = False
    
    # Check LLM Service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LLM_SERVICE_URL}/health", timeout=2.0)
            services_status["llm"] = response.status_code == 200
    except:
        services_status["llm"] = False
    
    # Check Storage Service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{STORAGE_SERVICE_URL}/health", timeout=2.0)
            services_status["storage"] = response.status_code == 200
    except:
        services_status["storage"] = False
    
    all_healthy = all(services_status.values())
    
    return JSONResponse({
        "status": "healthy" if all_healthy else "degraded",
        "services": services_status
    })

@app.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    """
    Upload invoice for processing
    
    Flow:
    1. Receive PDF/image
    2. Call OCR Service to extract text
    3. Call LLM Service to structure data
    4. Call Storage Service to save
    5. Return invoice ID and data
    """
    try:
        # Validate file
        if not file.filename:
            raise InvoiceScannerException("File must have a filename")
        
        logger.info(f"Processing upload: {file.filename}")
        
        # Read file
        contents = await file.read()
        
        if not contents:
            raise InvoiceScannerException("File is empty")
        
        # Step 1: Call OCR Service
        logger.info("Step 1: Calling OCR Service...")
        async with httpx.AsyncClient() as client:
            ocr_response = await client.post(
                f"{OCR_SERVICE_URL}/extract",
                files={"file": (file.filename, contents)},
                timeout=60.0
            )
        
        if ocr_response.status_code != 200:
            raise InvoiceScannerException(f"OCR Service error: {ocr_response.text}")
        
        ocr_data = ocr_response.json()
        extracted_text = ocr_data.get("text", "")
        
        if not extracted_text:
            raise InvoiceScannerException("No text extracted from image")
        
        logger.info(f"OCR extraction successful")
        
        # Step 2: Call LLM Service
        logger.info("Step 2: Calling LLM Service...")
        async with httpx.AsyncClient() as client:
            llm_response = await client.post(
                f"{LLM_SERVICE_URL}/structure",
                json={"text": extracted_text},
                timeout=60.0
            )
        
        if llm_response.status_code != 200:
            raise InvoiceScannerException(f"LLM Service error: {llm_response.text}")
        
        llm_data = llm_response.json()
        structured_data = llm_data.get("data", {})
        
        logger.info(f"LLM structuring successful")
        
        # Step 3: Call Storage Service
        logger.info("Step 3: Calling Storage Service...")
        async with httpx.AsyncClient() as client:
            storage_response = await client.post(
                f"{STORAGE_SERVICE_URL}/save",
                json={
                    "vendor": structured_data.get("vendor_name"),
                    "date": structured_data.get("invoice_date"),
                    "total": structured_data.get("total_amount"),
                    "subtotal": structured_data.get("subtotal_amount"),
                    "tax": structured_data.get("tax_amount"),
                    "items": structured_data.get("line_items", [])
                },
                timeout=30.0
            )
        
        if storage_response.status_code != 200:
            raise InvoiceScannerException(f"Storage Service error: {storage_response.text}")
        
        storage_data = storage_response.json()
        invoice_id = storage_data.get("invoice_id")
        
        logger.info(f"Invoice saved successfully, ID: {invoice_id}")
        
        return JSONResponse({
            "status": "success",
            "invoice_id": invoice_id,
            "filename": file.filename,
            "vendor": structured_data.get("vendor_name"),
            "date": structured_data.get("invoice_date"),
            "total": structured_data.get("total_amount"),
            "tax": structured_data.get("tax_amount"),
            "line_items": structured_data.get("line_items", [])
        })
    
    except InvoiceScannerException as e:
        logger.error(f"Application error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except httpx.TimeoutException as e:
        logger.error(f"Service timeout: {e}")
        raise HTTPException(status_code=504, detail="Service unavailable")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/status/{invoice_id}")
async def get_status(invoice_id: int):
    """Get invoice processing status"""
    try:
        logger.info(f"Getting status for invoice {invoice_id}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{STORAGE_SERVICE_URL}/invoice/{invoice_id}",
                timeout=10.0
            )
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Storage service error")
        
        return response.json()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/invoices")
async def list_invoices():
    """List all invoices"""
    try:
        logger.info("Listing all invoices")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{STORAGE_SERVICE_URL}/invoices",
                timeout=10.0
            )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Storage service error")
        
        return response.json()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing invoices: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run: python -m uvicorn src.api_gateway.main:app --port 8000 --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )