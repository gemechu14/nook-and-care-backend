from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.payment import Payment
from src.schemas.payment import PaymentCreate, PaymentUpdate


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):

    def get_by_provider(
        self, db: Session, provider_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.provider_id == provider_id)
            .order_by(Payment.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()


crud_payment = CRUDPayment(Payment)


