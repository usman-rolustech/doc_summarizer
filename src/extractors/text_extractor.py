"""Text extraction using unstructured library."""
from pathlib import Path
from typing import List
from unstructured.partition.auto import partition

from .base import BaseExtractor, ExtractionError
from ..utils.logger import setup_logger


class UnstructuredTextExtractor(BaseExtractor):
    """Text extractor using the unstructured library."""
    
    def __init__(self):
        super().__init__()
        self.logger = setup_logger(__name__)
    
    def extract(self, file_path: Path) -> str:
        """Extract text using unstructured library.
        
        Args:
            file_path: Path to the file to extract text from
            
        Returns:
            Extracted text as string
            
        Raises:
            ExtractionError: If extraction fails
        """
        try:
            self.logger.info(f"Extracting text from '{file_path}' using unstructured...")
            
            elements = partition(filename=str(file_path))
            extracted_text = "\n\n".join([str(el) for el in elements])
            
            self.logger.info(f"Successfully extracted {len(extracted_text)} characters")
            return extracted_text
            
        except Exception as e:
            error_msg = f"Unstructured extraction failed for '{file_path}': {e}"
            self.logger.error(error_msg)
            raise ExtractionError(error_msg) from e
    
    def can_extract(self, file_path: Path) -> bool:
        """Check if unstructured can handle this file type."""
        # Unstructured supports many formats, so we'll be permissive
        supported_extensions = ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt']
        return file_path.suffix.lower() in supported_extensions