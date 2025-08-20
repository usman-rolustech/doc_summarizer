# Document Summarizer

A robust Python application that extracts text from various document formats and generates intelligent summaries using Azure OpenAI. The application supports multiple extraction methods including the unstructured library and OCR fallback for challenging documents.

## Features

- **Multi-format Support**: PDF, DOC, DOCX, TXT, and more
- **Intelligent Text Extraction**: Uses unstructured library with OCR fallback
- **Azure OpenAI Integration**: Generates high-quality summaries using GPT models
- **Robust Error Handling**: Graceful fallbacks and detailed logging
- **Modular Architecture**: Clean, maintainable codebase with proper separation of concerns
- **Configuration Management**: Environment-based configuration with validation

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI API access
- Tesseract OCR installed on your system

### Installing Tesseract OCR

#### Windows
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Or use: `choco install tesseract` (if using Chocolatey)

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd document-summarizer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

## Configuration

Create a `.env` file in the root directory with your Azure OpenAI credentials:

```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_API_VERSION=2024-05-01-preview
AZURE_OPENAI_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

### Optional Configuration

You can customize the application behavior by modifying `config/settings.py`:

- `OCR_MIN_TEXT_LENGTH`: Minimum text length before falling back to OCR
- `SUMMARY_TEMPERATURE`: Control creativity in summaries (0.0-1.0)
- `SUMMARY_MAX_TOKENS`: Maximum tokens in generated summaries
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Usage

### Basic Usage

```bash
python main.py "path/to/your/document.pdf"
```

### Examples

```bash
# Summarize a PDF
python main.py "reports/quarterly-report.pdf"

# Summarize a Word document
python main.py "documents/meeting-notes.docx"

# Summarize a text file
python main.py "notes/research-notes.txt"
```

### Output

The application will:
1. Extract text from your document
2. Generate a comprehensive summary
3. Display the summary in the terminal
4. Save the summary to a file (e.g., `document_summary.txt`)

## Project Structure

```
document-summarizer/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .env                     # Your environment variables (not in git)
├── .gitignore               # Git ignore rules
├── main.py                  # Main application entry point
├── config/
│   └── settings.py          # Configuration management
├── src/
│   ├── extractors/          # Text extraction modules
│   │   ├── base.py          # Base extractor interface
│   │   ├── text_extractor.py # Unstructured library extractor
│   │   └── ocr_extractor.py  # OCR-based extractor
│   ├── summarizers/         # Summarization modules
│   │   └── azure_openai_summarizer.py # Azure OpenAI summarizer
│   └── utils/               # Utility modules
│       ├── file_utils.py    # File handling utilities
│       └── logger.py        # Logging setup
├── tests/                   # Test files (for future development)
└── docs/                    # Additional documentation
```

## How It Works

1. **File Validation**: Checks if the file exists and has a supported format
2. **Text Extraction**: 
   - First tries the unstructured library for clean text extraction
   - Falls back to OCR if extraction yields insufficient text
3. **Summarization**: Sends extracted text to Azure OpenAI for intelligent summarization
4. **Output**: Saves summary to file and displays in terminal

##
