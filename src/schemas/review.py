from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ReviewBase(BaseModel):
    listing_id: uuid.UUID
    rating: int
    comment: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("rating must be between 1 and 5")
        return v


class ReviewCreate(ReviewBase):
    tour_id: Optional[uuid.UUID] = None
    user_id: uuid.UUID


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
    response_from_provider: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not 1 <= v <= 5:
            raise ValueError("rating must be between 1 and 5")
        return v


class ReviewRead(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tour_id: Optional[uuid.UUID] = None
    user_id: uuid.UUID
    response_from_provider: Optional[str] = None
    created_at: datetime
    updated_at: datetime





