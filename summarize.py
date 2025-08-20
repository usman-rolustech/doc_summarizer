import os
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI
from unstructured.partition.auto import partition

# OCR imports
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Load environment variables
load_dotenv()

# --- DEBUG: Print env vars to verify they're loaded ---
print("Loaded environment variables:")
print("AZURE_OPENAI_API_KEY:", os.getenv("AZURE_OPENAI_API_KEY"))
print("AZURE_OPENAI_API_VERSION:", os.getenv("AZURE_OPENAI_API_VERSION"))
print("AZURE_OPENAI_ENDPOINT:", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("AZURE_OPENAI_DEPLOYMENT:", os.getenv("AZURE_OPENAI_DEPLOYMENT"))
print("---------------------------------------------------\n")

def extract_text_with_ocr(file_path):
    """
    Extracts text from each page of a PDF using OCR.
    """
    print(f"Running OCR on '{file_path}'...")
    images = convert_from_path(file_path)
    ocr_text = []
    for i, img in enumerate(images, start=1):
        print(f"OCR on page {i}/{len(images)}...")
        text = pytesseract.image_to_string(img)
        ocr_text.append(text)
    return "\n\n".join(ocr_text)

def extract_text_from_file(file_path):
    """
    Extract text using unstructured, fallback to OCR if needed.
    """
    try:
        print(f"Extracting text from '{file_path}'...")
        elements = partition(filename=file_path)
        extracted_text = "\n\n".join([str(el) for el in elements])
        print("Text extraction complete.")

        # If extracted text is too short, fallback to OCR
        if len(extracted_text.strip()) < 500:  
            print("Extracted text seems too short. Falling back to OCR...")
            extracted_text = extract_text_with_ocr(file_path)

        return extracted_text
    except Exception as e:
        print(f"Unstructured extraction failed: {e}. Falling back to OCR...")
        return extract_text_with_ocr(file_path)

def summarize_text(document_text, client, deployment_name):
    """
    Summarizes the given text using Azure OpenAI.
    """
    try:
        print("Connecting to Azure OpenAI and generating summary...")

        prompt = (
            f"Summarize the following document (including any OCR-extracted chart or table text):\n\n"
            f"---\n\n{document_text}\n\n---\n\nSummary:"
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are an expert assistant skilled at summarizing documents, charts, and financial data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )

        summary = response.choices[0].message.content.strip()
        print("Summary generation complete.")
        return summary

    except Exception as e:
        return f"An error occurred during summarization: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize.py \"<path_to_document>\"")
        sys.exit(1)

    document_path = sys.argv[1]

    try:
        # Extract text (with OCR fallback)
        text_to_summarize = extract_text_from_file(document_path)

        if not text_to_summarize.strip():
            print("The document appears empty or contains no extractable text.")
            sys.exit(1)

        # Azure client
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        # Summarize
        summary_result = summarize_text(text_to_summarize, client, deployment_name)

        # Save summary
        output_file = os.path.splitext(document_path)[0] + "_summary.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary_result)

        print("\n--- Summary ---\n")
        print(summary_result)
        print(f"\nSummary saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{document_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
