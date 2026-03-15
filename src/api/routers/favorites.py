from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.core.dependencies import DBSession, PaginationParams
from src.crud.crud_favorite import crud_favorite
from src.schemas.favorite import FavoriteCreate, FavoriteRead

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get("/", response_model=List[FavoriteRead])
def list_favorites(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_favorite.get_all(db, skip=skip, limit=limit)


@router.get("/{favorite_id}", response_model=FavoriteRead)
def get_favorite(favorite_id: uuid.UUID, db: DBSession):
    fav = crud_favorite.get_by_id(db, favorite_id)
    if fav is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    return fav


@router.post("/", response_model=FavoriteRead, status_code=201)
def add_favorite(payload: FavoriteCreate, db: DBSession):
    # Prevent duplicate favorites
    existing = crud_favorite.get_by_user_and_listing(
        db, payload.user_id, payload.listing_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Listing already in favorites",
        )
    return crud_favorite.create(db, payload)


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(favorite_id: uuid.UUID, db: DBSession):
    deleted = crud_favorite.delete(db, favorite_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")


