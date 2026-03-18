from __future__ import annotations

import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.crud.base import CRUDBase
from src.models.favorite import Favorite
from src.models.listing import Listing
from src.schemas.favorite import FavoriteCreate, FavoriteRead


class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, FavoriteRead]):

    def get_by_user(
        self, db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Favorite]:
        stmt = (
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_favorited_listings_by_user(
        self, db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .join(Favorite, Favorite.listing_id == Listing.id)
            .where(Favorite.user_id == user_id)
            .options(selectinload(Listing.images))
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_by_user_and_listing(
        self, db: Session, user_id: uuid.UUID, listing_id: uuid.UUID
    ) -> Optional[Favorite]:
        stmt = select(Favorite).where(
            Favorite.user_id == user_id, Favorite.listing_id == listing_id
        )
        return db.execute(stmt).scalar_one_or_none()


crud_favorite = CRUDFavorite(Favorite)







