from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.tour import Tour
from src.schemas.tour import TourCreate, TourUpdate


class CRUDTour(CRUDBase[Tour, TourCreate, TourUpdate]):

    def get_by_listing(
        self, db: Session, listing_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Tour]:
        stmt = (
            select(Tour)
            .where(Tour.listing_id == listing_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_by_user(
        self, db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Tour]:
        stmt = (
            select(Tour)
            .where(Tour.booked_by_user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()


crud_tour = CRUDTour(Tour)





