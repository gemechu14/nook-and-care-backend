from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InsuranceOptionBase(BaseModel):
    name: str
    description: Optional[str] = None


class InsuranceOptionCreate(InsuranceOptionBase):
    pass


class InsuranceOptionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class InsuranceOptionRead(InsuranceOptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class ListingInsuranceOptionBase(BaseModel):
    listing_id: uuid.UUID
    insurance_option_id: uuid.UUID


class ListingInsuranceOptionCreate(ListingInsuranceOptionBase):
    pass


class ListingInsuranceOptionRead(ListingInsuranceOptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


