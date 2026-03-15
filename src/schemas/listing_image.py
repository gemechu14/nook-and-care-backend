from __future__ import annotations

import base64
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ListingImageBase(BaseModel):
    display_order: int = 0
    is_primary: bool = False
    # Support both URL and binary storage
    image_url: Optional[str] = None
    # Note: Database schema only has: id, listing_id, image_url, display_order, is_primary, created_at
    # filename, content_type, and file_size are not in the database but can be accepted in API for processing


class ListingImageCreate(ListingImageBase):
    listing_id: uuid.UUID
    # For file uploads: base64-encoded image data
    image_data_base64: Optional[str] = None

    @field_validator("image_data_base64", mode="before")
    @classmethod
    def validate_image_data(cls, v: Optional[str]) -> Optional[str]:
        if v:
            # Remove data URL prefix if present (e.g., "data:image/jpeg;base64,...")
            if "," in v:
                v = v.split(",", 1)[1]
            try:
                # Validate it's valid base64
                base64.b64decode(v, validate=True)
            except Exception:
                raise ValueError("Invalid base64 image data")
        return v


class ListingImageUpdate(BaseModel):
    image_url: Optional[str] = None
    display_order: Optional[int] = None
    is_primary: Optional[bool] = None


class ListingImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    listing_id: uuid.UUID
    image_url: Optional[str] = None
    display_order: int
    is_primary: bool
    created_at: datetime
    # Note: filename, content_type, file_size are not in database but can be extracted from image_url if needed


# ── Batch Operations ────────────────────────────────────────────────────────────

class ListingImageBatchItem(BaseModel):
    listing_id: uuid.UUID
    image_data_base64: Optional[str] = None
    image_url: Optional[str] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    display_order: int = 0
    is_primary: bool = False

    @field_validator("image_data_base64", mode="before")
    @classmethod
    def validate_image_data(cls, v: Optional[str]) -> Optional[str]:
        if v:
            if "," in v:
                v = v.split(",", 1)[1]
            try:
                base64.b64decode(v, validate=True)
            except Exception:
                raise ValueError("Invalid base64 image data")
        return v
    
    def model_post_init(self, __context) -> None:
        """Ensure either image_url or image_data_base64 is provided."""
        if not self.image_url and not self.image_data_base64:
            raise ValueError("Either image_url or image_data_base64 must be provided")


class ListingImageBatchCreate(BaseModel):
    items: list[ListingImageBatchItem]


class ListingImageBatchDeleteItem(BaseModel):
    image_id: uuid.UUID


class ListingImageBatchDelete(BaseModel):
    items: list[ListingImageBatchDeleteItem]

