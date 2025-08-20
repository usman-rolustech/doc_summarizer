"""Configuration settings for the document summarizer."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AzureOpenAIConfig:
    """Azure OpenAI configuration."""
    
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        required_fields = ["API_KEY", "ENDPOINT", "DEPLOYMENT"]
        missing_fields = []
        
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(f"AZURE_OPENAI_{field}")
        
        if missing_fields:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")


class AppConfig:
    """Application configuration."""
    
    # OCR settings
    OCR_MIN_TEXT_LENGTH = 500
    
    # Summarization settings
    SUMMARY_TEMPERATURE = 0.5
    SUMMARY_MAX_TOKENS = 1500
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # File handling
    SUPPORTED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt']