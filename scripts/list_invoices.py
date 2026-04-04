"""
Invoice Scanner: CLI tool to list all invoices
Usage: python scripts/list_invoices.py
"""
import httpx
import sys
from config import SCRIPT_API_URL

def list_invoices():
    """List all invoices"""
    
    print("📋 Fetching invoices...")
    
    try:
        response = httpx.get(
            f"{SCRIPT_API_URL}/invoices",
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            invoices = data.get("invoices", [])
            
            if not invoices:
                print("No invoices found")
                return True
            
            print(f"\n✅ Found {len(invoices)} invoices:\n")
            print(f"{'ID':<5} {'Vendor':<30} {'Date':<12} {'Total':>10}")
            print("-" * 60)
            
            for inv in invoices:
                print(f"{inv['id']:<5} {inv['vendor']:<30} {inv['date']:<12} ${inv['total']:>9.2f}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    
    except httpx.ConnectError:
        print(f"❌ Cannot connect to API at {SCRIPT_API_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = list_invoices()
    sys.exit(0 if success else 1)