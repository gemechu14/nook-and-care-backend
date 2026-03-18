from __future__ import annotations

import uuid
from typing import Any, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.crud.base import CRUDBase
from src.models.tour import Tour
from src.schemas.tour import TourCreate, TourUpdate


class CRUDTour(CRUDBase[Tour, TourCreate, TourUpdate]):

    def get_by_id(self, db: Session, record_id: Any) -> Optional[Tour]:
        stmt = select(Tour).where(Tour.id == record_id).options(selectinload(Tour.booked_by))
        return db.execute(stmt).scalar_one_or_none()

    def get_all(self, db: Session, skip: int = 0, limit: int = 20) -> Sequence[Tour]:
        stmt = select(Tour).options(selectinload(Tour.booked_by)).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def get_by_listing(
        self, db: Session, listing_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Tour]:
        stmt = (
            select(Tour)
            .where(Tour.listing_id == listing_id)
            .options(selectinload(Tour.booked_by))
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
            .options(selectinload(Tour.booked_by))
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()


crud_tour = CRUDTour(Tour)







