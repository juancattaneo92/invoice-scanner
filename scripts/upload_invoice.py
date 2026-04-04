"""
Invoice Scanner: CLI tool to upload invoices
Usage: python scripts/upload_invoice.py path/to/invoice.pdf
"""
import sys
import httpx
from pathlib import Path
import argparse
from config import SCRIPT_API_URL, SCRIPT_VALID_EXTENSIONS


def validate_file(file_path: str) -> Path | None:
    """Validate file exists, is a file, and has a supported extension."""
    path = Path(file_path)

    if not path.exists():
        print(f"❌ Error: File not found: {path}")
        return None

    if not path.is_file():
        print(f"❌ Error: Not a file: {path}")
        return None

    if path.suffix.lower() not in SCRIPT_VALID_EXTENSIONS:
        print(f"❌ Error: Unsupported file type. Supported: {SCRIPT_VALID_EXTENSIONS}")
        return None

    return path


def send_file(path: Path) -> httpx.Response | None:
    """Send file to the upload API endpoint."""
    try:
        with open(path, "rb") as f:
            return httpx.post(
                f"{SCRIPT_API_URL}/upload",
                files={"file": (path.name, f)},
                timeout=120.0,
            )
    except httpx.ConnectError:
        print("❌ Error: Cannot connect to API")
        print("   Make sure API Gateway is running:")
        print("   python -m uvicorn src.api_gateway.main:app --port 8000")
        return None
    except httpx.TimeoutException:
        print("❌ Error: Request timeout. Processing took too long.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def print_result(response: httpx.Response) -> bool:
    """Print the API response and return success status."""
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Upload successful!")
        print(f"   Invoice ID: {data.get('invoice_id')}")
        print(f"   Vendor: {data.get('vendor')}")
        print(f"   Date: {data.get('date')}")
        print(f"   Total: ${(data.get('total') or 0):.2f}")
        return True

    print(f"❌ Upload failed: {response.status_code}")
    try:
        detail = response.json().get('detail', response.text)
    except Exception:
        detail = response.text
    print(f"   {detail}")
    return False


def upload_invoice(file_path: str) -> bool:
    """Upload invoice to API."""
    path = validate_file(file_path)
    if path is None:
        return False

    print(f"📤 Uploading {path.name}...")

    response = send_file(path)
    if response is None:
        return False

    return print_result(response)


def main():
    parser = argparse.ArgumentParser(description="Upload invoice for processing")
    parser.add_argument("file", help="Path to invoice file (PDF or image)")

    args = parser.parse_args()

    success = upload_invoice(args.file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
