from __future__ import annotations

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.core.dependencies import CurrentUserID, DBSession, PaginationParams, http_bearer
from src.crud.crud_listing import crud_listing
from src.schemas.listing import ListingCreate, ListingRead, ListingListRead, ListingUpdate
from src.services import listing_service

router = APIRouter(prefix="/listings", tags=["Listings"])


@router.get("/", response_model=List[ListingListRead])
def list_listings(
    db: DBSession,
    pagination: PaginationParams,
    city: Optional[str] = Query(None),
    care_type: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    status: Optional[str] = Query(None, description="Filter by status: ACTIVE, INACTIVE, PENDING, SUSPENDED"),
):
    skip, limit = pagination
    return listing_service.search_listings(
        db,
        city=city,
        care_type=care_type,
        min_price=min_price,
        max_price=max_price,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.get("/featured", response_model=List[ListingRead])
def featured_listings(
    db: DBSession,
    pagination: PaginationParams,
    status: Optional[str] = Query(None, description="Filter by status: ACTIVE, INACTIVE, PENDING, SUSPENDED"),
):
    skip, limit = pagination
    return crud_listing.get_featured(db, skip=skip, limit=limit, status=status)


@router.get("/me", response_model=List[ListingListRead], dependencies=[Depends(http_bearer)])
def my_listings(db: DBSession, pagination: PaginationParams, user_id: CurrentUserID):
    skip, limit = pagination
    return listing_service.get_listings_for_user(db, uuid.UUID(user_id), skip=skip, limit=limit)


@router.get("/{listing_id}", response_model=ListingRead)
def get_listing(listing_id: uuid.UUID, db: DBSession):
    listing = crud_listing.get_by_id(db, listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    return listing


@router.post("/", response_model=ListingRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_listing(payload: ListingCreate, db: DBSession):
    return listing_service.create_listing(db, payload)


@router.put("/{listing_id}", response_model=ListingRead, dependencies=[Depends(http_bearer)])
def update_listing(listing_id: uuid.UUID, payload: ListingUpdate, db: DBSession):
    return listing_service.update_listing(db, listing_id, payload)


@router.post("/{listing_id}/activate", response_model=ListingRead, dependencies=[Depends(http_bearer)])
def activate_listing(listing_id: uuid.UUID, db: DBSession):
    """Admin: activate a listing."""
    return listing_service.activate_listing(db, listing_id)


@router.post("/{listing_id}/feature", response_model=ListingRead, dependencies=[Depends(http_bearer)])
def feature_listing(listing_id: uuid.UUID, db: DBSession, is_featured: bool = True):
    return listing_service.feature_listing(db, listing_id, is_featured)


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(http_bearer)])
def delete_listing(listing_id: uuid.UUID, db: DBSession):
    deleted = crud_listing.delete(db, listing_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")


