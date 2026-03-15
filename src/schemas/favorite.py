from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavoriteBase(BaseModel):
    user_id: uuid.UUID
    listing_id: uuid.UUID


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteRead(FavoriteBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime



