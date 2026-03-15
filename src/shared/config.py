"""
Invoice Parser: Configuration and environment variables
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