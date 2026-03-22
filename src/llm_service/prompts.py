"""
Invoice Scanner: System prompts powered by AI to extract data from invoices
"""

INVOICE_EXTRACTION_PROMPT = """
You are an expert at extracting structured data from invoice text.

Extract the following information from the invoice text below:
1. vendor_name: Name of the company billing the invoice
2. invoice_date: Date of the invoice (format: YYYY-MM-DD)
3. invoice_number: Invoice or reference number
4. total_amount: Total amount due
5. tax_amount: Tax amount (if available)
6. subtotal_amount: Subtotal before tax (if available)
7. line_items: List of items with description, quantity, unit price, and line total

Return ONLY valid JSON, no markdown or extra text.

Invoice Text:
{text}

Return JSON in this exact format:
{{
  "vendor_name": "string",
  "invoice_date": "YYYY-MM-DD",
  "invoice_number": "string",
  "total_amount": float,
  "tax_amount": float or null,
  "subtotal_amount": float or null,
  "line_items": [
    {{
      "description": "string",
      "quantity": number,
      "unit_price": float,
      "line_total": float
    }}
  ]ß
}}
"""

def get_extraction_prompt(text: str) -> str:
    """Get invoice extraction prompt"""
    return INVOICE_EXTRACTION_PROMPT.format(text=text)