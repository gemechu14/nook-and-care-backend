from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubscriptionBase(BaseModel):
    provider_id: uuid.UUID
    plan_type: str  # FREE | PRO | PREMIUM
    price: Optional[float] = None
    billing_cycle: str = "MONTHLY"  # MONTHLY | YEARLY
    start_date: date
    end_date: Optional[date] = None


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    plan_type: Optional[str] = None
    price: Optional[float] = None
    billing_cycle: Optional[str] = None
    end_date: Optional[date] = None
    status: Optional[str] = None


class SubscriptionRead(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime





