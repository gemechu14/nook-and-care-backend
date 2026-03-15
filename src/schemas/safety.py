from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SafetyFeatureBase(BaseModel):
    name: str
    category: str  # EMERGENCY | FIRE | ACCESSIBILITY | MEDICAL
    description: Optional[str] = None


class SafetyFeatureCreate(SafetyFeatureBase):
    pass


class SafetyFeatureUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


class SafetyFeatureRead(SafetyFeatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class ListingSafetyFeatureBase(BaseModel):
    listing_id: uuid.UUID
    safety_feature_id: uuid.UUID


class ListingSafetyFeatureCreate(ListingSafetyFeatureBase):
    pass


class ListingSafetyFeatureRead(ListingSafetyFeatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# ── Batch Operations ────────────────────────────────────────────────────────────

class ListingSafetyFeatureBatchItem(BaseModel):
    listing_id: uuid.UUID
    safety_feature_id: uuid.UUID


class ListingSafetyFeatureBatchCreate(BaseModel):
    items: list[ListingSafetyFeatureBatchItem]


class ListingSafetyFeatureBatchDelete(BaseModel):
    items: list[ListingSafetyFeatureBatchItem]





