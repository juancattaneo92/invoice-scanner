# Invoice Scanner

A modular, microservices-based invoice processing system using:
Python, FastAPI, PaddleOCR, and local Llama models.

## Architecture

- **API Gateway** (Port 8000): Main entry point
- **OCR Service** (Port 8001): Extract text from images/PDFs
- **LLM Service** (Port 8002): Structure extracted text
- **Storage Service** (Port 8003): Database operations

## Prerequisites
 
Before starting, please ensure you have:
 
### 1. Python 3.12+ (Required)
**macOS:**
```bash
# Download Python 3.12 from: https://www.python.org/downloads/
# Download the macOS 64-bit universal2 installer
# Verify installation:
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 --version
# Expected: Python 3.12.x
```
 
**Note:** Python 3.13 has compatibility issues with pydantic-core. Use Python 3.12.
 
### 2. Rust (Required for building dependencies)
**macOS:**
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
 
# Add Rust to your current shell session
export PATH="$HOME/.cargo/bin:$PATH"
 
# Verify installation
rustc --version
cargo --version
# Expected: rustc <version>, cargo <version>
```
 
### 3. Ollama (Required for local LLM)
```bash
# Download & Install from: https://ollama.ai
# Verify installation:
ollama --version
# Expected: ollama version is <version>
```
 
## Quick Start
### 0. Startup & Testing Guide available at each service folder at config.py
 
### 1. Clone and Navigate
```bash
git clone https://github.com/juancattaneo92/invoice-scanner.git
cd invoice-scanner
```
 
### 2. Create Virtual Environment
```bash
# Use Python 3.12 specifically
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv venv
 
# Activate virtual environment
source venv/bin/activate
 
# Verify correct Python version
python --version
# Expected: Python 3.12.x
```
 
### 3. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip
 
# Install all dependencies
pip install -r requirements.txt
```
 
### 4. Download Ollama Model
```bash
# Start Ollama in a separate terminal (keep running)
ollama serve
 
# In another terminal, pull the model (one-time)
ollama pull llama2
```

### 4. Architecture

## Module 1: Shared Utilities
```bash
- config.py - Loads environment variables
- exceptions.py - Custom error classes
- logger.py - Logging setup
- models.py - Data validation schemas (Pydantic)
- __init__.py - Package exports
```

## Module 2: OCR Service
```bash
- config.py - Loads OCR environment variables
- processor.py - Extracts text from PDFs and images with PaddleOCR
- main.py - API entry point with FastAPI application
- __init__.py - Package exports
```

## Module 3: LLM Service
```bash
- config.py - Loads LLM environment variables (model, temperature, port)
- prompts.py - System prompts for invoice data extraction
- processor.py - Calls Ollama and parses JSON responses with validation
- main.py - API entry point with FastAPI application
- __init__.py - Package exports
```

## Module 4: Storage Service
```bash
- config.py - Loads Storage environment variables and SQLite settings
- database.py - SQLAlchemy engine setup and session management
- models.py - ORM models for invoices and line items tables
- queries.py - Database CRUD operations (create, get, list invoices)
- main.py - API entry point with FastAPI application
- __init__.py - Package exports
```

## Module 5: API Gateway
```bash
- main.py - Orchestrates OCR → LLM → Storage pipeline, exposes unified API
- __init__.py - Package exports
```

## Running the Services

Each service runs in its own terminal. Start them in order:

**Terminal 1 — Ollama (LLM backend):**
```bash
ollama serve
```

**Terminal 2 — OCR Service:**
```bash
source venv/bin/activate
python -m uvicorn src.ocr_service.main:app --port 8001 --reload
```

**Terminal 3 — LLM Service:**
```bash
source venv/bin/activate
python -m uvicorn src.llm_service.main:app --port 8002 --reload
```

**Terminal 4 — Storage Service:**
```bash
source venv/bin/activate
python -m uvicorn src.storage_service.main:app --port 8003 --reload
```

**Terminal 5 — API Gateway:**
```bash
source venv/bin/activate
python -m uvicorn src.api_gateway.main:app --port 8000 --reload
```

**Verify all services are up:**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
    "status": "healthy",
    "services": {
        "ocr": true,
        "llm": true,
        "storage": true
    }
}
```

## API Endpoints

All requests go through the API Gateway on port 8000.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome / version info |
| GET | `/health` | Health check for all services |
| POST | `/upload` | Upload invoice file for processing |
| GET | `/status/{invoice_id}` | Get invoice by ID |
| GET | `/invoices` | List all invoices |

### Upload an invoice
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@path/to/invoice.pdf"
```

Supported formats: `.pdf`, `.jpg`, `.jpeg`, `.png`, `.tiff`

Example response:
```json
{
    "status": "success",
    "invoice_id": 1,
    "filename": "invoice.pdf",
    "vendor": "Acme Corp",
    "date": "2024-01-15",
    "total": 250.00,
    "tax": 25.00,
    "line_items": []
}
```

### List all invoices
```bash
curl http://localhost:8000/invoices
```

### Get invoice by ID
```bash
curl http://localhost:8000/status/1
```

## CLI Scripts

Run these from the `scripts/` directory with the virtual environment activated.

### Upload an invoice
```bash
cd scripts
python upload_invoice.py path/to/invoice.pdf
```

### Check invoice status
```bash
cd scripts
python check_status.py 1
```

### List all invoices
```bash
cd scripts
python list_invoices.py
```

## Project Structure

```
invoice-scanner/
├── src/
│   ├── shared/              # Shared utilities across all services
│   │   ├── config.py        # Service URLs and environment variables
│   │   ├── exceptions.py    # Custom exception classes
│   │   ├── logger.py        # Logging configuration
│   │   └── models.py        # Pydantic data models
│   ├── api_gateway/         # Port 8000 - Main entry point
│   │   └── main.py
│   ├── ocr_service/         # Port 8001 - Text extraction
│   │   ├── config.py
│   │   ├── processor.py
│   │   └── main.py
│   ├── llm_service/         # Port 8002 - Data structuring
│   │   ├── config.py
│   │   ├── prompts.py
│   │   ├── processor.py
│   │   └── main.py
│   └── storage_service/     # Port 8003 - Database operations
│       ├── config.py
│       ├── database.py
│       ├── models.py
│       ├── queries.py
│       └── main.py
├── scripts/                 # CLI tools
│   ├── config.py
│   ├── upload_invoice.py
│   ├── check_status.py
│   └── list_invoices.py
├── tests/
├── requirements.txt
└── README.md
```

## Troubleshooting

- **Port already in use:** `lsof -i :<port>` then `kill -9 <PID>`
- **PaddleOCR slow on first start:** Normal — downloads ~200MB of models once
- **LLM not responding:** Make sure `ollama serve` is running and `llama2` is pulled
- **Database not created:** Ensure the `data/` directory exists and is writable
- **Low OCR confidence:** Image may be blurry or low resolution
