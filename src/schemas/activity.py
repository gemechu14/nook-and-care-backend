from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    name: str
    category: str  # RECREATIONAL | SOCIAL | FITNESS | EDUCATIONAL
    description: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


class ActivityRead(ActivityBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class ListingActivityBase(BaseModel):
    listing_id: uuid.UUID
    activity_id: uuid.UUID


class ListingActivityCreate(ListingActivityBase):
    pass


class ListingActivityRead(ListingActivityBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime



