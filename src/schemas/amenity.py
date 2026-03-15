from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Amenity ────────────────────────────────────────────────────────────────────

class AmenityBase(BaseModel):
    name: str
    category: str  # BASIC | PREMIUM | SAFETY | ACCESSIBILITY
    icon: Optional[str] = None


class AmenityCreate(AmenityBase):
    pass


class AmenityUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None


class AmenityRead(AmenityBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# ── ListingAmenity ─────────────────────────────────────────────────────────────

class ListingAmenityBase(BaseModel):
    listing_id: uuid.UUID
    amenity_id: uuid.UUID


class ListingAmenityCreate(ListingAmenityBase):
    pass


class ListingAmenityRead(ListingAmenityBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


