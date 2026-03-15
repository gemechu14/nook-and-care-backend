from __future__ import annotations

import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.favorite import Favorite
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

    def get_by_user_and_listing(
        self, db: Session, user_id: uuid.UUID, listing_id: uuid.UUID
    ) -> Optional[Favorite]:
        stmt = select(Favorite).where(
            Favorite.user_id == user_id, Favorite.listing_id == listing_id
        )
        return db.execute(stmt).scalar_one_or_none()


crud_favorite = CRUDFavorite(Favorite)



