from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CertificationBase(BaseModel):
    name: str
    description: Optional[str] = None


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CertificationRead(CertificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class ListingCertificationBase(BaseModel):
    listing_id: uuid.UUID
    certification_id: uuid.UUID
    license_number: Optional[str] = None


class ListingCertificationCreate(ListingCertificationBase):
    pass


class ListingCertificationUpdate(BaseModel):
    license_number: Optional[str] = None


class ListingCertificationRead(ListingCertificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


