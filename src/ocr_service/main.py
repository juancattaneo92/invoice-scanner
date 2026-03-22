"""
Invoice Scanner: OCR Service - FastAPI application
Extracts text from PDFs and images
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from src.shared.logger import logger
from src.shared.exceptions import OCRException
from src.ocr_service.processor import ocr_processor
from src.ocr_service.config import SERVICE_PORT, SERVICE_NAME, SERVICE_DESCRIPTION, SERVICE_API_VERSION, SERVICE_TITLE 
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info(f"{SERVICE_NAME} starting on port {SERVICE_PORT}")
    yield
    # Shutdown (if needed)
    logger.info(f"{SERVICE_NAME} shutting down")

app = FastAPI(
    title=SERVICE_TITLE,
    description=SERVICE_DESCRIPTION,
    VERSION=SERVICE_API_VERSION,
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": SERVICE_NAME
    }

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    """
    Extract text from uploaded file (PDF or image)
    
    Args:
        file: Uploaded PDF or image file
        
    Returns:
        Extracted text and metadata
    """
    try:
        # Validate filename
        if not file.filename:
            raise OCRException("File must have a filename")
        
        # Read file
        contents = await file.read()
        
        if not contents:
            raise OCRException("Uploaded file is empty")
        
        logger.info(f"Processing upload: {file.filename}")
        
        # Process OCR
        result = ocr_processor.extract_text(contents, file.filename)
        
        return JSONResponse({
            "status": "success",
            "filename": file.filename,
            "text": result["text"],
            "confidence": result["confidence"],
            "pages": result["pages"]
        })
    
    except OCRException as e:
        logger.error(f"OCR error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error in OCR: {e}")
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