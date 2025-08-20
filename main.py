#!/usr/bin/env python3
"""
Document Summarizer - Main Entry Point

This script extracts text from documents and generates summaries using Azure OpenAI.
It supports text extraction via unstructured library with OCR fallback.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from config.settings import AppConfig, AzureOpenAIConfig
from src.extractors.text_extractor import UnstructuredTextExtractor
from src.extractors.ocr_extractor import OCRExtractor
from src.extractors.base import ExtractionError
from src.summarizers.azure_openai_summarizer import AzureOpenAISummarizer
from src.utils.file_utils import validate_file_path, generate_output_path, save_text_to_file
from src.utils.logger import setup_logger


def extract_text_from_document(file_path: Path) -> str:
    """Extract text from document using multiple extraction methods.
    
    Args:
        file_path: Path to the document
        
    Returns:
        Extracted text
        
    Raises:
        ExtractionError: If all extraction methods fail
    """
    logger = setup_logger(__name__)
    
    # Try unstructured first
    text_extractor = UnstructuredTextExtractor()
    try:
        extracted_text = text_extractor.extract(file_path)
        
        # Check if extracted text is sufficient
        if len(extracted_text.strip()) >= AppConfig.OCR_MIN_TEXT_LENGTH:
            logger.info("Successfully extracted text using unstructured library")
            return extracted_text
        else:
            logger.warning(f"Extracted text too short ({len(extracted_text)} chars). Trying OCR...")
    
    except ExtractionError:
        logger.warning("Unstructured extraction failed. Trying OCR...")
    
    # Fallback to OCR
    ocr_extractor = OCRExtractor()
    if ocr_extractor.can_extract(file_path):
        try:
            extracted_text = ocr_extractor.extract(file_path)
            logger.info("Successfully extracted text using OCR")
            return extracted_text
        except ExtractionError:
            logger.error("OCR extraction also failed")
    
    raise ExtractionError("All extraction methods failed")


def main():
    """Main function."""
    logger = setup_logger(__name__)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<path_to_document>\"")
        print("\nSupported file types:", ", ".join(AppConfig.SUPPORTED_EXTENSIONS))
        sys.exit(1)
    
    document_path_str = sys.argv[1]
    
    try:
        # Validate input file
        document_path = validate_file_path(document_path_str)
        logger.info(f"Processing document: {document_path}")
        
        # Extract text
        logger.info("Starting text extraction...")
        extracted_text = extract_text_from_document(document_path)
        
        if not extracted_text.strip():
            logger.error("The document appears empty or contains no extractable text.")
            sys.exit(1)
        
        logger.info(f"Successfully extracted {len(extracted_text)} characters")
        
        # Initialize summarizer
        logger.info("Initializing Azure OpenAI summarizer...")
        summarizer = AzureOpenAISummarizer()
        
        if not summarizer.is_available():
            logger.error("Azure OpenAI summarizer is not available. Check your configuration.")
            sys.exit(1)
        
        # Generate summary
        logger.info("Generating summary...")
        summary = summarizer.summarize(extracted_text)
        
        # Save summary
        output_path = generate_output_path(document_path)
        save_text_to_file(summary, output_path)
        
        # Display results
        print("\n" + "="*50)
        print("DOCUMENT SUMMARY")
        print("="*50)
        print(summary)
        print("="*50)
        print(f"\nSummary saved to: {output_path}")
        
        logger.info("Document summarization completed successfully")
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except ExtractionError as e:
        logger.error(f"Text extraction error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()