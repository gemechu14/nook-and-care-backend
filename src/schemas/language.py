from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LanguageBase(BaseModel):
    code: str
    name: str


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None


class LanguageRead(LanguageBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class ListingLanguageBase(BaseModel):
    listing_id: uuid.UUID
    language_id: uuid.UUID


class ListingLanguageCreate(ListingLanguageBase):
    pass


class ListingLanguageRead(ListingLanguageBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


# ── Batch Operations ────────────────────────────────────────────────────────────

class ListingLanguageBatchItem(BaseModel):
    listing_id: uuid.UUID
    language_id: uuid.UUID


class ListingLanguageBatchCreate(BaseModel):
    items: list[ListingLanguageBatchItem]


class ListingLanguageBatchDelete(BaseModel):
    items: list[ListingLanguageBatchItem]





