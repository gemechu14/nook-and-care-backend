from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReportBase(BaseModel):
    report_type: str  # FAKE_LISTING | SCAM_PROVIDER | MISLEADING_IMAGES | FRAUD | OTHER
    description: str
    reported_user_id: Optional[uuid.UUID] = None
    listing_id: Optional[uuid.UUID] = None


class ReportCreate(ReportBase):
    reported_by_user_id: uuid.UUID


class ReportUpdate(BaseModel):
    status: Optional[str] = None  # PENDING | REVIEWED | RESOLVED | DISMISSED


class ReportRead(ReportBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    reported_by_user_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime







