"""
Invoice Scanner: Database queries and operations
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.storage_service.models import Invoice, LineItem
from src.shared.logger import logger
from src.shared.exceptions import DatabaseException
from src.shared.models import InvoiceCreate

class InvoiceQueries:
    """Database operations for invoices"""
    
    @staticmethod
    def create_invoice(db: Session, invoice_data: InvoiceCreate) -> Invoice:
        """Create new invoice"""
        try:
            invoice = Invoice(
                vendor=invoice_data.vendor,
                date=invoice_data.date,
                total=invoice_data.total,
                subtotal=invoice_data.subtotal,
                tax=invoice_data.tax
            )
            
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            
            logger.info(f"Created invoice ID: {invoice.id}, Vendor: {invoice.vendor}")
            
            # Create line items if provided
            if invoice_data.items:
                for item in invoice_data.items:
                    line_item = LineItem(
                        invoice_id=invoice.id,
                        description=item.get("description", ""),
                        quantity=item.get("quantity", 1),
                        unit_price=item.get("unit_price", 0),
                        line_total=item.get("line_total", 0)
                    )
                    db.add(line_item)
                
                db.commit()
                logger.info(f"Created {len(invoice_data.items)} line items for invoice {invoice.id}")
            
            return invoice
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create invoice: {e}")
            raise DatabaseException(f"Failed to create invoice: {e}")
    
    @staticmethod
    def get_invoice(db: Session, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        try:
            invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
            
            if not invoice:
                logger.warning(f"Invoice not found: {invoice_id}")
                return None
            
            return invoice
    
        except Exception as e:
            logger.error(f"Failed to get invoice: {e}")
            raise DatabaseException(f"Failed to get invoice: {e}")
        
    @staticmethod
    def get_all_invoices(db: Session, limit: int = 100) -> list:
        """Get all invoices"""
        try:
            invoices = db.query(Invoice).order_by(desc(Invoice.created_at)).limit(limit).all()
            return invoices
        
        except Exception as e:
            logger.error(f"Failed to get invoices: {e}")
            raise DatabaseException(f"Failed to get invoices: {e}")

# Create instance for use
invoice_queries = InvoiceQueries()