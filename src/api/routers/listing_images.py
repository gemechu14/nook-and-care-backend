from __future__ import annotations

import base64
import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import Response

from src.core.dependencies import DBSession, http_bearer
from src.crud.crud_listing_image import crud_listing_image
from src.schemas.listing_image import ListingImageCreate, ListingImageRead, ListingImageUpdate

# Allowed image MIME types
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/bmp",
}

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

router = APIRouter(prefix="/listing-images", tags=["Listing Images"])


@router.get("/", response_model=List[ListingImageRead])
def list_images(db: DBSession):
    return crud_listing_image.get_all(db)


@router.get("/listing/{listing_id}", response_model=List[ListingImageRead])
def get_images_by_listing(listing_id: uuid.UUID, db: DBSession):
    """Get all images for a specific listing."""
    return crud_listing_image.get_by_listing(db, listing_id)


@router.get("/{image_id}", response_model=ListingImageRead)
def get_image(image_id: uuid.UUID, db: DBSession):
    """Get image metadata."""
    img = crud_listing_image.get_by_id(db, image_id)
    if img is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return img


@router.get("/{image_id}/download")
def download_image(image_id: uuid.UUID, db: DBSession):
    """Download image binary data. Use this URL directly in HTML <img> tags.
    
    Example:
        <img src="/api/v1/listing-images/{image_id}/download" alt="Listing image" />
    """
    img = crud_listing_image.get_by_id(db, image_id)
    if img is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    if not img.image_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image data not available"
        )

    content_type = img.content_type or "image/jpeg"
    headers = {
        "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
    }
    if img.filename:
        headers["Content-Disposition"] = f'inline; filename="{img.filename}"'

    return Response(content=img.image_data, media_type=content_type, headers=headers)


@router.post("/upload", response_model=ListingImageRead, status_code=201, dependencies=[Depends(http_bearer)])
async def upload_image(
    listing_id: Annotated[uuid.UUID, Form(description="Listing ID to attach the image to")],
    file: Annotated[UploadFile, File(description="Image file to upload (JPEG, PNG, GIF, WebP, BMP)")],
    display_order: Annotated[int, Form(description="Display order (lower numbers appear first)", ge=0)] = 0,
    is_primary: Annotated[bool, Form(description="Whether this is the primary image")] = False,
    db: DBSession = ...,
):
    """Upload an image file directly from device and store it in the database.
    
    Supports common image formats: JPEG, PNG, GIF, WebP, BMP
    Maximum file size: 10MB
    
    The image is stored as binary data in the database and can be retrieved via the download endpoint.
    """
    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    # Read file content
    file_content = await file.read()
    
    # Validate file size
    file_size = len(file_content)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024):.0f}MB"
        )
    
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )

    # Encode to base64 for the schema
    image_data_base64 = base64.b64encode(file_content).decode("utf-8")

    # Create image record
    payload = ListingImageCreate(
        listing_id=listing_id,
        image_data_base64=image_data_base64,
        filename=file.filename,
        content_type=file.content_type,
        display_order=display_order,
        is_primary=is_primary,
    )

    return crud_listing_image.create(db, payload)


@router.post("/", response_model=ListingImageRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_image(payload: ListingImageCreate, db: DBSession):
    """Create an image record (supports base64 data or URL)."""
    return crud_listing_image.create(db, payload)


@router.put("/{image_id}", response_model=ListingImageRead, dependencies=[Depends(http_bearer)])
def update_image(image_id: uuid.UUID, payload: ListingImageUpdate, db: DBSession):
    img = crud_listing_image.get_by_id(db, image_id)
    if img is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return crud_listing_image.update(db, img, payload)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(http_bearer)])
def delete_image(image_id: uuid.UUID, db: DBSession):
    deleted = crud_listing_image.delete(db, image_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

