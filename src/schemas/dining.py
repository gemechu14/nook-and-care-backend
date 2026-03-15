from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DiningOptionBase(BaseModel):
    name: str
    description: Optional[str] = None


class DiningOptionCreate(DiningOptionBase):
    pass


class DiningOptionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DiningOptionRead(DiningOptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class ListingDiningOptionBase(BaseModel):
    listing_id: uuid.UUID
    dining_option_id: uuid.UUID


class ListingDiningOptionCreate(ListingDiningOptionBase):
    pass


class ListingDiningOptionRead(ListingDiningOptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime





