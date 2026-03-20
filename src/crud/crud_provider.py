from __future__ import annotations

import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.provider import Provider
from src.schemas.provider import ProviderCreate, ProviderUpdate


class CRUDProvider(CRUDBase[Provider, ProviderCreate, ProviderUpdate]):

    def get_by_user_id(self, db: Session, user_id: uuid.UUID) -> Optional[Provider]:
        """Return the provider profile for this user.

        If multiple provider rows exist for the same ``user_id`` (legacy/duplicate data),
        returns the most recently created one instead of raising.
        """
        stmt = (
            select(Provider)
            .where(Provider.user_id == user_id)
            .order_by(Provider.created_at.desc())
            .limit(1)
        )
        return db.execute(stmt).scalars().first()

    def get_verified(self, db: Session, skip: int = 0, limit: int = 20) -> Sequence[Provider]:
        stmt = (
            select(Provider)
            .where(Provider.verification_status == "VERIFIED")
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()


crud_provider = CRUDProvider(Provider)







