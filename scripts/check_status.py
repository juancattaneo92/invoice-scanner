"""
Invoice Scanner: CLI tool to check invoice status
Usage: python scripts/check_status.py 1
"""
import sys
import httpx
import argparse
from config import SCRIPT_API_URL

def check_status(invoice_id: int):
    """Check status of invoice"""
    
    print(f"📋 Checking status for invoice {invoice_id}...")
    
    try:
        response = httpx.get(
            f"{SCRIPT_API_URL}/status/{invoice_id}",
            timeout=10.0
        )
        
        if response.status_code == 404:
            print(f"❌ Invoice not found: {invoice_id}")
            return False
        
        if response.status_code == 200:
            data = response.json().get("data", {})
            
            print(f"\n✅ Invoice {invoice_id}")
            print(f"   Vendor: {data.get('vendor')}")
            print(f"   Date: {data.get('date')}")
            print(f"   Total: ${data.get('total', 0):.2f}")
            print(f"   Status: {data.get('status')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.json().get('detail', response.text)}")
            return False
    
    except httpx.ConnectError:
        print(f"❌ Cannot connect to API at {SCRIPT_API_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Check invoice processing status")
    parser.add_argument("invoice_id", type=int, help="Invoice ID")
    
    args = parser.parse_args()
    
    success = check_status(args.invoice_id)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()