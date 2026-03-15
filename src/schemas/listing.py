from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    care_type: str  # ASSISTED_LIVING | MEMORY_CARE | INDEPENDENT_LIVING | ADULT_FAMILY_HOME | SKILLED_NURSING
    room_type: str  # PRIVATE | SEMI_PRIVATE | SHARED
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price: Optional[float] = None
    currency: str = "USD"
    capacity: Optional[int] = None
    available_beds: Optional[int] = None
    staff_ratio: Optional[str] = None
    established_year: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    license_number: Optional[str] = None
    is_featured: bool = False
    has_24_hour_care: bool = False


class ListingCreate(ListingBase):
    provider_id: uuid.UUID


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    care_type: Optional[str] = None
    room_type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    capacity: Optional[int] = None
    available_beds: Optional[int] = None
    staff_ratio: Optional[str] = None
    established_year: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    license_number: Optional[str] = None
    is_featured: Optional[bool] = None
    has_24_hour_care: Optional[bool] = None
    status: Optional[str] = None


class ListingRead(ListingBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    provider_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime



