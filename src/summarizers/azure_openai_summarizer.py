"""Azure OpenAI-based text summarization."""
from openai import AzureOpenAI
from typing import Optional

from config.settings import AzureOpenAIConfig, AppConfig
from ..utils.logger import setup_logger


class AzureOpenAISummarizer:
    """Summarizer using Azure OpenAI."""
    
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Azure OpenAI client."""
        try:
            AzureOpenAIConfig.validate()
            
            self.client = AzureOpenAI(
                api_key=AzureOpenAIConfig.API_KEY,
                api_version=AzureOpenAIConfig.API_VERSION,
                azure_endpoint=AzureOpenAIConfig.ENDPOINT,
            )
            
            self.logger.info("Azure OpenAI client initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            raise
    
    def summarize(self, document_text: str, custom_prompt: Optional[str] = None) -> str:
        """Summarize the given document text.
        
        Args:
            document_text: Text to summarize
            custom_prompt: Optional custom prompt for summarization
            
        Returns:
            Summary text
            
        Raises:
            Exception: If summarization fails
        """
        try:
            self.logger.info("Generating summary using Azure OpenAI...")
            
            if custom_prompt:
                prompt = custom_prompt.format(document_text=document_text)
            else:
                prompt = self._build_default_prompt(document_text)
            
            response = self.client.chat.completions.create(
                model=AzureOpenAIConfig.DEPLOYMENT,
                messages=[
                    {
                        "role": "system", 
                            "content": "You are an expert assistant skilled at summarizing documents, charts, and financial data. You MUST provide summaries in exactly 4 sentences, no more, no less."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=AppConfig.SUMMARY_TEMPERATURE,
                max_tokens=AppConfig.SUMMARY_MAX_TOKENS
            )
            
            summary = response.choices[0].message.content.strip()
            self.logger.info(f"Summary generation complete. Generated {len(summary)} characters")
            return summary
            
        except Exception as e:
            error_msg = f"Summarization failed: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def _build_default_prompt(self, document_text: str) -> str:
        """Build the default summarization prompt."""
        return (
            f"Summarize the following document (including any OCR-extracted chart or table text):\n\n"
            f"---\n\n{document_text}\n\n---\n\n"
            f"Please provide a comprehensive summary that captures the key points, "
            f"main themes, and important details from the document. If there are any "
            f"charts, tables, or numerical data mentioned, please include those insights "
            f"in your summary as well.\n\nSummary:"
        )
    
    def is_available(self) -> bool:
        """Check if the summarizer is properly configured and available."""
        return self.client is not None