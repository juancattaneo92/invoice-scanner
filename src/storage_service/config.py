"""
Invoice Scanner: Storage Service configuration
"""

# Service settings
SERVICE_PORT = 8003
SERVICE_NAME = "storage_service"
SERVICE_SQL_ECHO = False  # Set to True for SQL debugging
SERVICE_CONNECT_ARGS = {"check_same_thread": False}  # Required for SQLite with SQLAlchemy

# Storage Service API metadata
SERVICE_TITLE = "Invoice Scanner Storage Service"
SERVICE_DESCRIPTION = "Manages invoice data in SQLite database"
SERVICE_API_VERSION = "1.0.0"

# ============================================
# STORAGE SERVICE - STARTUP & TESTING GUIDE
# ============================================

# To Start:
# 1. Activate virtual environment. Run: source venv/bin/activate
# 2. Start Storage Service. Run: python -m uvicorn src.storage_service.main:app --port 8003 --reload
#    Expected output:
#    INFO:     Uvicorn running on http://0.0.0.0:8003
#    2026-03-19 20:25:10 | INFO | storage_service.main - storage_service starting on port 8003
#    Creating database tables...

# To Stop:
# Ctrl+C in terminal where service is running

# To Test Health Endpoint:
# curl http://localhost:8003/health
# Or in browser: http://localhost:8003/health
# Expected response:
# {
#     "status": "healthy",
#     "service": "storage_service"
# }

# To Test Save Invoice:
# curl -X POST http://localhost:8003/save \
#   -H "Content-Type: application/json" \
#   -d '{
#     "vendor": "Test Corp",
#     "date": "2020-01-01",
#     "total": 100.00,
#     "subtotal": 90.00,
#     "tax": 10.00,
#     "items": []
#   }'
# Expected response:
# {
#     "status": "success",
#     "invoice_id": 1,
#     "vendor": "Test Corp",
#     "total": 100.00
# }

# To Test Get Invoice:
# curl http://localhost:8003/invoice/1
# Expected response:
# {
#     "status": "success",
#     "id": 1,
#     "vendor": "Test Corp",
#     "date": "2020-01-01",
#     "total": 100.00,
#     "status": "completed"
# }

# To Test List All Invoices:
# curl http://localhost:8003/invoices
# Expected response:
# {
#     "status": "success",
#     "count": 1,
#     "invoices": [
#         {
#             "id": 1,
#             "vendor": "Test Corp",
#             "date": "2020-01-01",
#             "total": 100.00,
#             "status": "completed"
#         }
#     ]
# }

# To View API Documentation:
# Open in browser: http://localhost:8003/docs
# You'll see Swagger UI with all endpoints

# To View Database File:
# ls -la data/invoices.db
# File location: data/invoices.db

# To Backup Database:
# cp data/invoices.db data/invoices.db.backup

# Troubleshooting:
# - "Address already in use" on port 8003:
#   Kill existing process: lsof -i :8003, then kill -9 <PID>
#
# - Database file not created:
#   Ensure data/ directory exists and is writable
#
# - "table invoices already exists" error:
#   Database was already initialized, this is normal
#
# - Can't save invoice (400 error):
#   Check that all required fields are present (vendor, date, total)