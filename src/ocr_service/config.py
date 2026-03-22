"""
Invoice Scanner: OCR Service configuration
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

# ============================================
# OCR SERVICE - STARTUP & TESTING GUIDE
# ============================================

# To Start:
# 1. Activate virtual environment. Run: source venv/bin/activate
# 2. Start OCR Service. Run: python -m uvicorn src.ocr_service.main:app --port 8001 --reload
#    Expected output:
#    INFO:     Uvicorn running on http://0.0.0.0:8001
#    2026-03-19 20:21:15 | INFO | ocr_service.main - ocr_service starting on port 8001

# To Stop:
# Ctrl+C in terminal where service is running

# To Test Health Endpoint:
# curl http://localhost:8001/health
# Or in browser: http://localhost:8001/health
# Expected response:
# {
#     "status": "healthy",
#     "service": "ocr_service"
# }

# To Test File Upload (Extract Text):
# curl -X POST http://localhost:8001/extract \
#   -F "file=@path/to/invoice.pdf"
# Expected response:
# {
#     "status": "success",
#     "filename": "invoice.pdf",
#     "text": "Invoice #123\nVendor: Acme Corp\n...",
#     "confidence": 0.92,
#     "pages": 1
# }

# To View API Documentation:
# Open in browser: http://localhost:8001/docs
# You'll see Swagger UI with all endpoints and can test directly

# To View ReDoc (Alternative API Documentation):
# Open in browser: http://localhost:8001/redoc

# Troubleshooting:
# - "Address already in use" on port 8001:
#   Kill existing process: lsof -i :8001, then kill -9 <PID>
#
# - PaddleOCR initialization slow first time:
#   Normal - downloads OCR models (~200MB), be patient
#
# - "file is empty" error:
#   Make sure you're uploading an actual PDF/image file
#
# - Low confidence scores:
#   Indicates unclear/blurry text - OCR had trouble reading it