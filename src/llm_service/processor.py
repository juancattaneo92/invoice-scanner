"""
Invoice Scanner: LLM Processing logic using Ollama
"""
import json
import re
import ollama
from src.shared.logger import logger
from src.shared.exceptions import LLMException
from src.llm_service.config import OLLAMA_MODEL, TEMPERATURE
from src.llm_service.prompts import get_extraction_prompt

class LLMProcessor:
    """Handles LLM operations"""
    
    def __init__(self):
        """Initialize LLM"""
        logger.info(f"Initializing Ollama with model: {OLLAMA_MODEL}")
        logger.info("Ollama initialized successfully")
    
    def extract_invoice_data(self, ocr_text: str) -> dict:
        """
        Extract structured invoice data from OCR text
        
        Args:
            ocr_text: Raw OCR extracted text
            
        Returns:
            Structured invoice data as dict
        """
        try:
            logger.info("Starting LLM extraction...")
            
            # Get prompt
            prompt = get_extraction_prompt(ocr_text)
            
            # Call Ollama
            response = ollama.generate(
                model=OLLAMA_MODEL,
                prompt=prompt,
                stream=False,
                options={
                    "temperature": TEMPERATURE,
                    "num_ctx": 4096
                }
            )
            
            # Extract response text
            response_text = response.get("response", "")
            logger.debug(f"Raw LLM response: {response_text[:200]}...")
            
            # Parse JSON from response
            extracted_data = self._parse_json_response(response_text)
            
            # Validate required fields
            self._validate_extracted_data(extracted_data)
            
            logger.info("LLM extraction completed successfully")
            return extracted_data
        
        except LLMException:
            raise
        except Exception as e:
            logger.error(f"LLM processing failed: {e}")
            raise LLMException(f"LLM processing failed: {e}")
    
    @staticmethod
    def _parse_json_response(response_text: str) -> dict:
        """
        Parse JSON from LLM response
        
        Handles cases where JSON might be embedded in markdown or extra text
        """
        try:
            # Try direct JSON parse
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON block in markdown
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to find any JSON-like object
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        raise LLMException("Could not parse JSON from LLM response")
    
    @staticmethod
    def _validate_extracted_data(data: dict) -> None:
        """Validate that required fields are present"""
        required_fields = ["vendor_name", "total_amount"]
        
        for field in required_fields:
            if field not in data or data[field] is None:
                raise LLMException(f"Missing required field: {field}")
        
        # Ensure total_amount is numeric
        try:
            float(data["total_amount"])
        except (TypeError, ValueError):
            raise LLMException("total_amount must be numeric")

# Create global processor instance
llm_processor = LLMProcessor()