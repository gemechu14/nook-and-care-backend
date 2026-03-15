from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TourBase(BaseModel):
    listing_id: uuid.UUID
    tour_type: str  # VIRTUAL | IN_PERSON
    scheduled_at: datetime


class TourCreate(TourBase):
    booked_by_user_id: Optional[uuid.UUID] = None


class TourUpdate(BaseModel):
    tour_type: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None


class TourRead(TourBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    booked_by_user_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime



