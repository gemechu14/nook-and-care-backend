from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RefreshTokenBase(BaseModel):
    user_id: uuid.UUID
    token: str
    expires_at: datetime


class RefreshTokenCreate(RefreshTokenBase):
    pass


class RefreshTokenRead(RefreshTokenBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_revoked: bool
    created_at: datetime



