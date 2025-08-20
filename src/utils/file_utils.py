"""File handling utilities."""
import os
from pathlib import Path
from typing import Tuple
from config.settings import AppConfig


def validate_file_path(file_path: str) -> Path:
    """Validate that the file exists and has a supported extension."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    if path.suffix.lower() not in AppConfig.SUPPORTED_EXTENSIONS:
        supported = ', '.join(AppConfig.SUPPORTED_EXTENSIONS)
        raise ValueError(f"Unsupported file type '{path.suffix}'. Supported types: {supported}")
    
    return path


def generate_output_path(input_path: Path, suffix: str = "_summary") -> Path:
    """Generate an output file path based on input path."""
    return input_path.parent / f"{input_path.stem}{suffix}.txt"


def save_text_to_file(text: str, output_path: Path) -> None:
    """Save text content to a file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes."""
    return file_path.stat().st_size / (1024 * 1024)