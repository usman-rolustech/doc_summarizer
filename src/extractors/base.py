"""Base classes for text extractors."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseExtractor(ABC):
    """Abstract base class for text extractors."""
    
    def __init__(self):
        self.logger = None
    
    @abstractmethod
    def extract(self, file_path: Path) -> str:
        """Extract text from the given file.
        
        Args:
            file_path: Path to the file to extract text from
            
        Returns:
            Extracted text as string
            
        Raises:
            ExtractionError: If extraction fails
        """
        pass
    
    def can_extract(self, file_path: Path) -> bool:
        """Check if this extractor can handle the given file type.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if this extractor can handle the file type
        """
        return True


class ExtractionError(Exception):
    """Exception raised when text extraction fails."""
    pass