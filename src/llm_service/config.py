"""
Invoice Scanner: LLM Service configuration
"""

# Ollama settings
OLLAMA_MODEL = "llama2"
TEMPERATURE = 0.1  # Lower = more deterministic
MAX_TOKENS = 500

# Service settings
SERVICE_PORT = 8002
SERVICE_NAME = "llm_service"

# FastAPI settings
FASTAPI_TITLE = "Invoice Scanner LLM Service"
FASTAPI_DESCRIPTION = "Structures invoice data using Ollama Llama2"
FASTAPI_VERSION = "1.0.0"

# ============================================
# LLM SERVICE - STARTUP & TESTING GUIDE
# ============================================

# To Start:
# 1. Activate virtual environment. Run: source venv/bin/activate
# 2. Make sure Ollama is running. Run: ollama serve (in separate terminal)
# 3. Start LLM Service. Run: python -m uvicorn src.llm_service.main:app --port 8002 --reload
#    Expected output:
#    INFO:     Uvicorn running on http://0.0.0.0:8002
#    2026-03-19 20:25:10 | INFO | llm_service.main - llm_service starting on port 8002

# To Stop:
# Ctrl+C in terminal where service is running

# To Test Health Endpoint:
# curl http://localhost:8002/health
# Or in browser: http://localhost:8002/health
# Expected response:
# {
#     "status": "healthy",
#     "service": "llm_service"
# }

# To Test Structure Extraction (Extract & Structure OCR Text):
# curl -X POST http://localhost:8002/structure \
#   -H "Content-Type: application/json" \
#   -d '{"text": "Invoice #123\nVendor: Test Corp\nTotal: $100"}'
# Expected response:
# {
#     "status": "success",
#     "data": {
#         "vendor_name": "Test Corp",
#         "invoice_date": "2020-01-01",
#         "invoice_number": "123",
#         "total_amount": 100.0,
#         "tax_amount": null,
#         "subtotal_amount": null,
#         "line_items": []
#     }
# }

# To View API Documentation:
# Open in browser: http://localhost:8002/docs
# You'll see Swagger UI with all endpoints and can test directly

# To View ReDoc (Alternative API Documentation):
# Open in browser: http://localhost:8002/redoc

# Troubleshooting:
# - "Failed to initialize Ollama" error:
#   Make sure ollama serve is running in separate terminal
#
# - "Could not parse JSON from LLM response":
#   Ollama response wasn't valid JSON - try with clearer text
#
# - Slow responses:
#   Llama2 is running locally - first request slower, then faster
#   Depends on your CPU/RAM
#
# - "Empty text provided" error:
#   Make sure you're sending non-empty text in the request