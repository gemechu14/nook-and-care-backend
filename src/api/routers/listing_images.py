from __future__ import annotations

import base64
import uuid
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import Response

from src.core.dependencies import DBSession
from src.crud.crud_listing_image import crud_listing_image
from src.schemas.listing_image import ListingImageCreate, ListingImageRead, ListingImageUpdate

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
    """Download image binary data."""
    img = crud_listing_image.get_by_id(db, image_id)
    if img is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    if not img.image_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image data not available"
        )

    content_type = img.content_type or "application/octet-stream"
    headers = {}
    if img.filename:
        headers["Content-Disposition"] = f'inline; filename="{img.filename}"'

    return Response(content=img.image_data, media_type=content_type, headers=headers)


@router.post("/upload", response_model=ListingImageRead, status_code=201)
async def upload_image(
    listing_id: uuid.UUID,
    file: UploadFile = File(...),
    display_order: int = 0,
    is_primary: bool = False,
    db: DBSession = ...,
):
    """Upload an image file and store it in the database."""
    # Read file content
    file_content = await file.read()

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


@router.post("/", response_model=ListingImageRead, status_code=201)
def create_image(payload: ListingImageCreate, db: DBSession):
    """Create an image record (supports base64 data or URL)."""
    return crud_listing_image.create(db, payload)


@router.put("/{image_id}", response_model=ListingImageRead)
def update_image(image_id: uuid.UUID, payload: ListingImageUpdate, db: DBSession):
    img = crud_listing_image.get_by_id(db, image_id)
    if img is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return crud_listing_image.update(db, img, payload)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(image_id: uuid.UUID, db: DBSession):
    deleted = crud_listing_image.delete(db, image_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

