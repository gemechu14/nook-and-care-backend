from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── TreatmentService ───────────────────────────────────────────────────────────

class TreatmentServiceBase(BaseModel):
    name: str
    description: Optional[str] = None


class TreatmentServiceCreate(TreatmentServiceBase):
    pass


class TreatmentServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TreatmentServiceRead(TreatmentServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# ── ListingService ─────────────────────────────────────────────────────────────

class ListingServiceBase(BaseModel):
    listing_id: uuid.UUID
    treatment_service_id: uuid.UUID
    price: Optional[float] = None
    is_included: bool = False


class ListingServiceCreate(ListingServiceBase):
    pass


class ListingServiceUpdate(BaseModel):
    price: Optional[float] = None
    is_included: Optional[bool] = None


class ListingServiceRead(ListingServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


