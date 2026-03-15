from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProviderBase(BaseModel):
    business_name: str
    business_type: str
    tax_id: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class ProviderCreate(ProviderBase):
    user_id: uuid.UUID


class ProviderUpdate(BaseModel):
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    verification_status: Optional[str] = None


class ProviderRead(ProviderBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    verification_status: str
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime





