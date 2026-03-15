"""File storage utilities for handling image uploads."""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Optional

from src.core.config import get_settings

settings = get_settings()


def ensure_upload_dir() -> Path:
    """Ensure the upload directory exists and return its Path."""
    upload_dir = Path(settings.UPLOAD_DIR) / "listing-images"
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def save_image_file(file_content: bytes, filename: Optional[str] = None, extension: Optional[str] = None) -> tuple[str, str]:
    """Save image file to disk and return (file_path, url_path).
    
    Args:
        file_content: Binary image data
        filename: Original filename (optional, used to determine extension)
        extension: File extension (optional, e.g., '.jpg')
    
    Returns:
        Tuple of (relative_file_path, url_path)
        - relative_file_path: Path relative to uploads directory (e.g., "listing-images/abc123.jpg")
        - url_path: URL path for serving (e.g., "/uploads/listing-images/abc123.jpg")
    """
    upload_dir = ensure_upload_dir()
    
    # Determine extension
    if not extension:
        if filename:
            extension = Path(filename).suffix.lower()
        else:
            extension = ".jpg"  # Default
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{extension}"
    file_path = upload_dir / unique_filename
    
    # Save file
    file_path.write_bytes(file_content)
    
    # Return relative path and URL path
    relative_path = f"listing-images/{unique_filename}"
    url_path = f"/uploads/{relative_path}"
    
    return relative_path, url_path


def delete_image_file(file_path: str) -> bool:
    """Delete an image file from disk.
    
    Args:
        file_path: Relative path from uploads directory (e.g., "listing-images/abc123.jpg")
    
    Returns:
        True if file was deleted, False if it didn't exist
    """
    upload_dir = Path(settings.UPLOAD_DIR)
    full_path = upload_dir / file_path
    
    if full_path.exists():
        full_path.unlink()
        return True
    return False


def get_image_url(image_url: Optional[str], file_path: Optional[str] = None) -> Optional[str]:
    """Get the image URL, preferring image_url over file_path.
    
    Args:
        image_url: External URL if provided
        file_path: Relative file path if image is stored locally
    
    Returns:
        URL string or None
    """
    if image_url:
        return image_url
    if file_path:
        return f"/uploads/{file_path}"
    return None

