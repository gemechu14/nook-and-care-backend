from __future__ import annotations

import uuid
from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.crud.crud_listing import crud_listing
from src.crud.crud_provider import crud_provider
from src.models.listing import Listing
from src.schemas.listing import ListingCreate, ListingUpdate

# Valid status transitions for a listing
_VALID_TRANSITIONS: dict[str, list[str]] = {
    "PENDING": ["ACTIVE", "REJECTED"],
    "ACTIVE": ["INACTIVE", "SUSPENDED"],
    "INACTIVE": ["ACTIVE"],
    "SUSPENDED": ["ACTIVE", "INACTIVE"],
    "REJECTED": [],
}


def create_listing(db: Session, payload: ListingCreate) -> Listing:
    """Create a new listing.

    Validates that the provider exists and is VERIFIED before creating.
    """
    provider = crud_provider.get_by_id(db, payload.provider_id)
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    if provider.verification_status != "VERIFIED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider must be verified before creating listings",
        )
    return crud_listing.create(db, payload)


def update_listing(
    db: Session, listing_id: uuid.UUID, payload: ListingUpdate
) -> Listing:
    listing = crud_listing.get_by_id(db, listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    # Validate status transition if status is being changed
    if payload.status and payload.status != listing.status:
        allowed = _VALID_TRANSITIONS.get(listing.status, [])
        if payload.status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition listing from {listing.status} to {payload.status}",
            )

    return crud_listing.update(db, listing, payload)


def activate_listing(db: Session, listing_id: uuid.UUID) -> Listing:
    """Admin: approve and activate a listing."""
    listing = crud_listing.get_by_id(db, listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    listing.status = "ACTIVE"
    db.commit()
    db.refresh(listing)
    return listing


def feature_listing(db: Session, listing_id: uuid.UUID, is_featured: bool) -> Listing:
    """Toggle featured status for a listing."""
    listing = crud_listing.get_by_id(db, listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    listing.is_featured = is_featured
    db.commit()
    db.refresh(listing)
    return listing


def search_listings(
    db: Session,
    city: Optional[str] = None,
    care_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 20,
) -> Sequence[Listing]:
    return crud_listing.search(
        db,
        city=city,
        care_type=care_type,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit,
    )


