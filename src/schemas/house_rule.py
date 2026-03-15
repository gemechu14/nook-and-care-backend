from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HouseRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str  # GENERAL | VISITOR | PET | SMOKING | QUIET_HOURS


class HouseRuleCreate(HouseRuleBase):
    pass


class HouseRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class HouseRuleRead(HouseRuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class ListingHouseRuleBase(BaseModel):
    listing_id: uuid.UUID
    house_rule_id: uuid.UUID
    display_order: int = 0


class ListingHouseRuleCreate(ListingHouseRuleBase):
    pass


class ListingHouseRuleUpdate(BaseModel):
    display_order: Optional[int] = None


class ListingHouseRuleRead(ListingHouseRuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


