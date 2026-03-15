from __future__ import annotations

import base64
import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import Response

from src.core.dependencies import CurrentUserID, DBSession, http_bearer
from src.crud.crud_listing_image import crud_listing_image
from src.crud.crud_listing import crud_listing
from src.crud.crud_provider import crud_provider
from src.crud.crud_user import get_by_id as get_user
from src.schemas.listing_image import (
    ListingImageBatchCreate,
    ListingImageBatchDelete,
    ListingImageCreate,
    ListingImageRead,
    ListingImageUpdate,
)

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


# ── Helper Functions ────────────────────────────────────────────────────────────

def verify_provider_owns_listing(
    db: DBSession, user_id: str, listing_id: uuid.UUID
) -> None:
    """Verify that the authenticated user (as a provider) owns the listing.
    
    Raises 403 if user is not a provider or doesn't own the listing.
    Raises 404 if listing doesn't exist.
    """
    user = get_user(db, user_id)
    if user is None or user.role not in ("PROVIDER", "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only providers and admins can manage listing images",
        )
    
    if user.role == "ADMIN":
        # Admins can manage any listing
        listing = crud_listing.get_by_id(db, listing_id)
        if listing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found",
            )
        return
    
    # For providers, verify ownership
    provider = crud_provider.get_by_user_id(db, uuid.UUID(user_id))
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Provider profile not found",
        )
    
    listing = crud_listing.get_by_id(db, listing_id)
    if listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    
    if listing.provider_id != provider.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage this listing",
        )


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
    from pathlib import Path
    from src.core.config import get_settings
    
    img = crud_listing_image.get_by_id(db, image_id)
    if img is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    # If image_url is a local file, serve it from disk
    if img.image_url and img.image_url.startswith("/uploads/"):
        settings = get_settings()
        relative_path = img.image_url.replace("/uploads/", "")
        file_path = Path(settings.UPLOAD_DIR) / relative_path
        
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Image file not found"
            )
        
        # Determine content type from file extension or default to jpeg
        content_type = "image/jpeg"  # Default
        if file_path.suffix.lower() in [".png"]:
            content_type = "image/png"
        elif file_path.suffix.lower() in [".gif"]:
            content_type = "image/gif"
        elif file_path.suffix.lower() in [".webp"]:
            content_type = "image/webp"
        elif file_path.suffix.lower() in [".bmp"]:
            content_type = "image/bmp"
        
        headers = {
            "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
        }
        
        return Response(content=file_path.read_bytes(), media_type=content_type, headers=headers)
    
    # If it's an external URL, redirect to it
    if img.image_url:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=img.image_url, status_code=302)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Image URL not available"
    )


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

    # Save file to disk and get URL
    from src.core.storage import save_image_file
    
    file_path, url_path = save_image_file(
        file_content,
        filename=file.filename
    )

    # Create image record with URL
    # Database only stores: listing_id, image_url, display_order, is_primary
    payload = ListingImageCreate(
        listing_id=listing_id,
        image_url=url_path,  # Store URL instead of base64
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


# ── Batch Operations ────────────────────────────────────────────────────────────

@router.post(
    "/batch",
    response_model=List[ListingImageRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch upload listing images",
    description="Upload multiple images for a listing in a single request. Supports base64-encoded image data or image URLs. All items must reference the same listing.",
    response_description="List of created listing image records",
)
def batch_upload_images(
    payload: ListingImageBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch upload listing images.
    
    - Requires authentication (Bearer token)
    - User must be a provider who owns the listing, or an admin
    - All items must reference the same listing
    - Supports base64-encoded image data or image URLs
    - Validates image data format and size
    """
    if not payload.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No items provided",
        )
    
    # Check all listing IDs are the same
    listing_ids = [item.listing_id for item in payload.items]
    first_listing_id = listing_ids[0]
    if not all(lid == first_listing_id for lid in listing_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All items must reference the same listing",
        )
    
    # Verify ownership
    verify_provider_owns_listing(db, user_id, first_listing_id)
    
    # Validate all items have either image_data_base64 or image_url
    for idx, item in enumerate(payload.items):
        if not item.image_data_base64 and not item.image_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item {idx}: Either image_data_base64 or image_url must be provided",
            )
        
        # Validate and save image data if provided
        item_file_size = None
        if item.image_data_base64:
            try:
                from src.core.storage import save_image_file
                
                # Remove data URL prefix if present
                image_data_str = item.image_data_base64
                if "," in image_data_str:
                    image_data_str = image_data_str.split(",", 1)[1]
                image_data = base64.b64decode(image_data_str)
                
                if len(image_data) > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Item {idx}: Image too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024):.0f}MB",
                    )
                if len(image_data) == 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Item {idx}: Image data is empty",
                    )
                
                # Save to disk and update item with URL
                file_path, url_path = save_image_file(
                    image_data,
                    filename=item.filename
                )
                item.image_url = url_path  # Replace base64 with URL
                item_file_size = len(image_data)  # Store file size
            except Exception as e:
                if isinstance(e, HTTPException):
                    raise e
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Item {idx}: Invalid image data format",
                )
        
        # Store file_size for later use
        item._file_size = item_file_size
    
    # Create all images
    created = []
    try:
        for item in payload.items:
            # Convert batch item to create schema
            # Note: image_data_base64 is now converted to image_url in validation above
            create_payload = ListingImageCreate(
                listing_id=item.listing_id,
                image_url=item.image_url,  # Use URL (either from file or external)
                display_order=item.display_order,
                is_primary=item.is_primary,
            )
            obj = crud_listing_image.create(db, create_payload)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create images: {str(e)}",
        )
    
    return created


@router.post(
    "/batch/upload",
    response_model=List[ListingImageRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch upload listing images (multipart/form-data)",
    description="Upload multiple image files for a listing using multipart/form-data. All files must be for the same listing.",
    response_description="List of created listing image records",
)
async def batch_upload_image_files(
    listing_id: Annotated[uuid.UUID, Form(description="Listing ID to attach images to")],
    files: Annotated[List[UploadFile], File(description="Image files to upload (JPEG, PNG, GIF, WebP, BMP)")],
    db: DBSession = ...,
    user_id: CurrentUserID = ...,
):
    """Batch upload image files using multipart/form-data.
    
    - Requires authentication (Bearer token)
    - User must be a provider who owns the listing, or an admin
    - Supports multiple files in a single request
    - Maximum file size: 10MB per file
    - Allowed formats: JPEG, PNG, GIF, WebP, BMP
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided",
        )
    
    # Verify ownership
    verify_provider_owns_listing(db, user_id, listing_id)
    
    # Validate and process all files
    file_data = []
    for file in files:
        # Validate file type
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type for {file.filename}. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size
        file_size = len(file_content)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File {file.filename} too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024):.0f}MB"
            )
        
        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File {file.filename} is empty"
            )
        
        # Save file to disk
        from src.core.storage import save_image_file
        
        file_path, url_path = save_image_file(
            file_content,
            filename=file.filename
        )
        
        file_data.append({
            "listing_id": listing_id,
            "image_url": url_path,  # Store URL instead of base64
            "display_order": len(file_data),  # Auto-increment display order
            "is_primary": len(file_data) == 0,  # First image is primary
        })
    
    # Create all images
    created = []
    try:
        for item_data in file_data:
            create_payload = ListingImageCreate(**item_data)
            obj = crud_listing_image.create(db, create_payload)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create images: {str(e)}",
        )
    
    return created


@router.delete(
    "/batch",
    response_model=List[ListingImageRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing images",
    description="Delete multiple listing images in a single request. Only images belonging to listings owned by the authenticated provider can be deleted.",
    response_description="List of deleted listing image records",
)
def batch_delete_images(
    payload: ListingImageBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing images.
    
    - Requires authentication (Bearer token)
    - User must be a provider who owns the listing, or an admin
    - Verifies ownership for each image's listing
    - Returns only successfully deleted items
    """
    if not payload.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No items provided",
        )
    
    from src.models.listing_image import ListingImage
    
    deleted = []
    listings_verified = {}  # Cache verified listings
    
    try:
        for item in payload.items:
            # Get image
            img = crud_listing_image.get_by_id(db, item.image_id)
            if img is None:
                continue  # Skip if image doesn't exist
            
            # Verify ownership (cache results)
            if img.listing_id not in listings_verified:
                verify_provider_owns_listing(db, user_id, img.listing_id)
                listings_verified[img.listing_id] = True
            
            # Delete image (CRUD delete will also delete file from disk)
            deleted_img = crud_listing_image.delete(db, img.id)
            if deleted_img:
                deleted.append(deleted_img)
        
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete images: {str(e)}",
        )
    
    return deleted

