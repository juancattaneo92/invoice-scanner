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