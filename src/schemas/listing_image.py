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
    filename: Optional[str] = None
    content_type: Optional[str] = None


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
    image_data_base64: Optional[str] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    display_order: Optional[int] = None
    is_primary: Optional[bool] = None


class ListingImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    listing_id: uuid.UUID
    image_url: Optional[str] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    file_size: Optional[int] = None
    display_order: int
    is_primary: bool
    created_at: datetime

    # Include image data as base64 for API responses (optional, can be large)
    image_data_base64: Optional[str] = None

    @classmethod
    def from_orm_with_data(cls, obj) -> "ListingImageRead":
        """Create a ListingImageRead instance including base64-encoded image data."""
        data = cls.model_validate(obj).model_dump()
        if obj.image_data:
            data["image_data_base64"] = base64.b64encode(obj.image_data).decode("utf-8")
        return cls(**data)

