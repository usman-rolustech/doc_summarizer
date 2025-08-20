"""OCR-based text extraction."""
from pathlib import Path
from typing import List
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

from .base import BaseExtractor, ExtractionError
from ..utils.logger import setup_logger


class OCRExtractor(BaseExtractor):
    """OCR-based text extractor for PDFs and images."""
    
    def __init__(self):
        super().__init__()
        self.logger = setup_logger(__name__)
    
    def extract(self, file_path: Path) -> str:
        """Extract text using OCR.
        
        Args:
            file_path: Path to the file to extract text from
            
        Returns:
            Extracted text as string
            
        Raises:
            ExtractionError: If OCR extraction fails
        """
        try:
            if file_path.suffix.lower() == '.pdf':
                return self._extract_from_pdf(file_path)
            else:
                return self._extract_from_image(file_path)
                
        except Exception as e:
            error_msg = f"OCR extraction failed for '{file_path}': {e}"
            self.logger.error(error_msg)
            raise ExtractionError(error_msg) from e
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF using OCR."""
        self.logger.info(f"Running OCR on PDF '{file_path}'...")
        
        images = convert_from_path(str(file_path))
        ocr_text = []
        
        total_pages = len(images)
        for i, img in enumerate(images, start=1):
            self.logger.info(f"OCR on page {i}/{total_pages}...")
            text = pytesseract.image_to_string(img)
            ocr_text.append(text)
        
        result = "\n\n".join(ocr_text)
        self.logger.info(f"OCR completed. Extracted {len(result)} characters from {total_pages} pages")
        return result
    
    def _extract_from_image(self, file_path: Path) -> str:
        """Extract text from image using OCR."""
        self.logger.info(f"Running OCR on image '{file_path}'...")
        
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        
        self.logger.info(f"OCR completed. Extracted {len(text)} characters")
        return text
    
    def can_extract(self, file_path: Path) -> bool:
        """Check if OCR can handle this file type."""
        ocr_extensions = [ '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        return file_path.suffix.lower() in ocr_extensions