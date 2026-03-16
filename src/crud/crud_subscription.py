from __future__ import annotations

import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.subscription import Subscription
from src.schemas.subscription import SubscriptionCreate, SubscriptionUpdate


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):

    def get_active_by_provider(
        self, db: Session, provider_id: uuid.UUID
    ) -> Optional[Subscription]:
        stmt = select(Subscription).where(
            Subscription.provider_id == provider_id,
            Subscription.status == "ACTIVE",
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_by_provider(
        self, db: Session, provider_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Subscription]:
        stmt = (
            select(Subscription)
            .where(Subscription.provider_id == provider_id)
            .order_by(Subscription.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()


crud_subscription = CRUDSubscription(Subscription)






