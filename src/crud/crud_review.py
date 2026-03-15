from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.review import Review
from src.schemas.review import ReviewCreate, ReviewUpdate


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):

    def get_by_listing(
        self, db: Session, listing_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Review]:
        stmt = (
            select(Review)
            .where(Review.listing_id == listing_id)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_by_user(
        self, db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Review]:
        stmt = (
            select(Review)
            .where(Review.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()


crud_review = CRUDReview(Review)



