"""
Invoice Parser: LLM Service - FastAPI application
Structures OCR text into invoice data using Ollama
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.shared.logger import logger
from src.shared.exceptions import LLMException
from src.llm_service.processor import llm_processor
from src.llm_service.config import SERVICE_PORT, SERVICE_NAME, FASTAPI_TITLE, FASTAPI_DESCRIPTION, FASTAPI_VERSION

class ExtractionRequest(BaseModel):
    """Request model for extraction"""
    text: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info(f"{SERVICE_NAME} starting on port {SERVICE_PORT}")
    yield
    # Shutdown
    logger.info(f"{SERVICE_NAME} shutting down")

# Create FastAPI app
app = FastAPI(
    title=FASTAPI_TITLE,
    description=FASTAPI_DESCRIPTION,
    version=FASTAPI_VERSION,
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": SERVICE_NAME
    }

@app.post("/structure")
async def structure_invoice_data(request: ExtractionRequest):
    """
    Structure OCR text into invoice data
    
    Args:
        request: Contains OCR extracted text
        
    Returns:
        Structured invoice data
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            raise LLMException("Empty text provided")
        
        logger.info("Processing LLM extraction request")
        
        # Extract structured data
        extracted_data = llm_processor.extract_invoice_data(request.text)
        
        return JSONResponse({
            "status": "success",
            "data": extracted_data
        })
    
    except LLMException as e:
        logger.error(f"LLM error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error in LLM: {e}")
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