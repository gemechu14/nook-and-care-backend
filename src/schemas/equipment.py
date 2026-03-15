from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EquipmentBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


class EquipmentRead(EquipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class ListingEquipmentBase(BaseModel):
    listing_id: uuid.UUID
    equipment_id: uuid.UUID
    quantity: int = 1


class ListingEquipmentCreate(ListingEquipmentBase):
    pass


class ListingEquipmentUpdate(BaseModel):
    quantity: Optional[int] = None


class ListingEquipmentRead(ListingEquipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# ── Batch Operations ────────────────────────────────────────────────────────────

class ListingEquipmentBatchItem(BaseModel):
    listing_id: uuid.UUID
    equipment_id: uuid.UUID
    quantity: int = 1


class ListingEquipmentBatchCreate(BaseModel):
    items: list[ListingEquipmentBatchItem]


class ListingEquipmentBatchDeleteItem(BaseModel):
    listing_id: uuid.UUID
    equipment_id: uuid.UUID


class ListingEquipmentBatchDelete(BaseModel):
    items: list[ListingEquipmentBatchDeleteItem]





