"""
Invoice Scanner: Configuration and environment variables
This file loads all environment variables from .env file 
and makes them accessible throughout the entire application
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Service URLs
OCR_SERVICE_URL = os.getenv("OCR_SERVICE_URL", "http://localhost:8001")
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8002")
STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL", "http://localhost:8003")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/invoices.db")

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

__all__ = [
    "API_HOST",
    "API_PORT",
    "OCR_SERVICE_URL",
    "LLM_SERVICE_URL",
    "STORAGE_SERVICE_URL",
    "DATABASE_URL",
    "OLLAMA_BASE_URL",
    "OLLAMA_MODEL",
    "LOG_LEVEL",
]

# ============================================
# SHARED UTILITIES - STARTUP & TESTING GUIDE
# ============================================
# To Test Config:
# python -c "from src.shared.config import API_HOST, API_PORT; print(f'API: {API_HOST}:{API_PORT}')"
# Expected: API: 0.0.0.0:8000

# To Test Logger:
# python << 'EOF'
# from src.shared.logger import logger
# logger.info("✅ Logger working!")
# logger.error("Test error")
# EOF
# Expected: Colored output in terminal + messages in logs/app.log

# To Test Exceptions:
# python -c "from src.shared.exceptions import OCRException; print('✅ Exceptions imported')"
# Expected: ✅ Exceptions imported

# To Test Models:
# python << 'EOF'
# from src.shared.models import InvoiceCreate
# invoice = InvoiceCreate(vendor="Test", date="2024-01-15", total=100.0)
# print(f"✅ Models working: {invoice.vendor}")
# EOF
# Expected: ✅ Models working: Test

# To Test All Shared Utilities Together:
# python -c "from src.shared import API_HOST, logger, InvoiceCreate, OCRException; print('✅ Shared utilities working!')"
# Expected: ✅ Shared utilities working!

# View Log File:
# cat logs/app.log