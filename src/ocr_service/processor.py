"""
Invoice Scanner: OCR Processing logic using PaddleOCR
"""
import tempfile
from pathlib import Path
from paddleocr import PaddleOCR
from src.shared.logger import logger
from src.shared.exceptions import OCRException
from src.ocr_service.config import USE_ANGLE_CLASSIFICATION, OCR_LANGUAGE

class OCRProcessor:
    """Handles OCR operations"""
    
    def __init__(self):
        """Initialize PaddleOCR"""
        try:
            logger.info("Initializing PaddleOCR...")
            self.ocr = PaddleOCR(
                use_angle_cls=USE_ANGLE_CLASSIFICATION,
                lang=OCR_LANGUAGE
            )
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PaddleOCR: {e}")
            raise OCRException(f"Failed to initialize OCR: {e}")
    
    def extract_text(self, file_bytes: bytes, filename: str) -> dict:
        """
        Extract text from image or PDF
        
        Args:
            file_bytes: File content as bytes
            filename: Original filename
            
        Returns:
            dict with extracted text and metadata
        """
        temp_file = None
        try:
            # Step 1: Save uploaded bytes to temporary file
            temp_file = self._save_to_temp_file(file_bytes)
            logger.info(f"Processing file: {filename}")
            
            # Step 2: Run OCR on the file
            result = self._run_ocr(temp_file)
            
            # Step 3: Check if we got any results
            if not result or not result[0]:
                logger.warning(f"No text extracted from {filename}")
                return self._empty_result()
            
            # Step 4: Extract text from all pages
            combined_text = self._extract_combined_text(result)
            
            # Step 5: Calculate confidence score
            avg_confidence = self._calculate_confidence(result)
            
            logger.info(f"Successfully extracted text from {filename}")
            logger.debug(f"Extracted {len(combined_text)} characters, confidence: {avg_confidence:.2f}")
            
            return {
                "text": combined_text,
                "confidence": float(avg_confidence),
                "pages": len(result)
            }
        
        except Exception as e:
            logger.error(f"OCR processing failed for {filename}: {e}")
            raise OCRException(f"OCR processing failed: {e}")
        
        finally:
            # Clean up temp file
            self._cleanup_temp_file(temp_file)
    
    def _save_to_temp_file(self, file_bytes: bytes) -> str:
        """
        Save file bytes to a temporary file
        
        Args:
            file_bytes: Raw file content
            
        Returns:
            Path to temporary file
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            return tmp.name
    
    def _run_ocr(self, file_path: str) -> list:
        """
        Run PaddleOCR on a file
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Raw OCR result from PaddleOCR
        """
        return self.ocr.ocr(file_path, cls=True)
    
    def _empty_result(self) -> dict:
        """
        Return an empty result when no text is found
        
        Returns:
            Empty result dictionary
        """
        return {
            "text": "",
            "confidence": 0.0,
            "pages": 0
        }
    
    def _extract_combined_text(self, result: list) -> str:
        """
        Extract text from all pages and combine them
        
        Args:
            result: Raw OCR result from PaddleOCR
            
        Returns:
            Combined text from all pages
        """
        all_text = []
        
        # Loop through each page
        for page_result in result:
            # Extract text from each line in the page
            page_text = "\n".join([
                line[0][0] for line in page_result if line and len(line) > 0
            ])
            all_text.append(page_text)
        
        # Join all pages with a page break separator
        combined_text = "\n---PAGE BREAK---\n".join(all_text)
        return combined_text
    
    def _calculate_confidence(self, result: list) -> float:
        """
        Calculate average confidence score from OCR results
        
        Args:
            result: Raw OCR result from PaddleOCR
            
        Returns:
            Average confidence score (0.0 to 1.0)
        """
        confidences = []
        
        # Extract confidence from each detected line
        for page in result:
            for line in page:
                if line and len(line) > 1:
                    confidences.append(line[1])
        
        # Calculate average
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
        else:
            avg_confidence = 0.0
        
        return avg_confidence
    
    def _cleanup_temp_file(self, temp_file: str | None) -> None:
        """
        Delete temporary file if it exists
        
        Args:
            temp_file: Path to file to delete (can be None)
        """
        if temp_file and Path(temp_file).exists():
            try:
                Path(temp_file).unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_file}: {e}")

# Create global processor instance
ocr_processor = OCRProcessor()