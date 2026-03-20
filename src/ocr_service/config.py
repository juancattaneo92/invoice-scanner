"""
Invoice Parser: OCR Service configuration
This file loads all environment variables from .env file
and makes them accessible throughout the OCR service
"""

USE_ANGLE_CLASSIFICATION = True
OCR_LANGUAGE = "en"
OCR_ENABLED_CUDA = False

SERVICE_PORT = 8001
SERVICE_NAME = "ocr_service"
SERVICE_TITLE = "OCR Service"
SERVICE_DESCRIPTION = "OCR Service to extract text from PDFs and images using PaddleOCR"
SERVICE_API_VERSION = "1.0.0"

# To Start:
# 1. Acvivate virtual environment. Run: source venv/bin/activate
# 2. Start OCR Service. Run: python -m uvicorn src.ocr_service.main:app --port 8001 --reload

# To Stop:
# Ctrl+C in terminal where service is running

# To Test:
# curl http://localhost:8001/health
# In terminal:  http://localhost:8001/health
# View API