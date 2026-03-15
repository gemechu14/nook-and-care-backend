from __future__ import annotations

import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.listing import Listing
from src.schemas.listing import ListingCreate, ListingUpdate


class CRUDListing(CRUDBase[Listing, ListingCreate, ListingUpdate]):

    def get_by_provider(
        self, db: Session, provider_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .where(Listing.provider_id == provider_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_active(self, db: Session, skip: int = 0, limit: int = 20) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .where(Listing.status == "ACTIVE")
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_featured(self, db: Session, skip: int = 0, limit: int = 20) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .where(Listing.status == "ACTIVE", Listing.is_featured.is_(True))
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def search(
        self,
        db: Session,
        city: Optional[str] = None,
        care_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Listing]:
        stmt = select(Listing).where(Listing.status == "ACTIVE")
        if city:
            stmt = stmt.where(Listing.city.ilike(f"%{city}%"))
        if care_type:
            stmt = stmt.where(Listing.care_type == care_type)
        if min_price is not None:
            stmt = stmt.where(Listing.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Listing.price <= max_price)
        stmt = stmt.offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()


crud_listing = CRUDListing(Listing)



