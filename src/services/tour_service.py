from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.crud.crud_listing import crud_listing
from src.crud.crud_tour import crud_tour
from src.models.tour import Tour
from src.schemas.tour import TourCreate, TourUpdate

# Allowed tour status transitions
_VALID_TRANSITIONS: dict[str, list[str]] = {
    "PENDING": ["APPROVED", "CANCELLED"],
    "APPROVED": ["SCHEDULED", "CANCELLED"],
    "SCHEDULED": ["COMPLETED", "CANCELLED"],
    "COMPLETED": [],
    "CANCELLED": [],
}


def book_tour(db: Session, payload: TourCreate) -> Tour:
    """Book a tour for a listing.

    Validates that the listing is ACTIVE before booking.
    """
    listing = crud_listing.get_by_id(db, payload.listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    if listing.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Listing is not available for tours",
        )
    return crud_tour.create(db, payload)


def update_tour_status(
    db: Session, tour_id: uuid.UUID, new_status: str
) -> Tour:
    """Transition a tour to a new status.

    Enforces allowed state transitions.
    """
    tour = crud_tour.get_by_id(db, tour_id)
    if tour is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tour not found")

    allowed = _VALID_TRANSITIONS.get(tour.status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition tour from {tour.status} to {new_status}",
        )

    tour.status = new_status
    db.commit()
    db.refresh(tour)
    return tour


def cancel_tour(db: Session, tour_id: uuid.UUID) -> Tour:
    return update_tour_status(db, tour_id, "CANCELLED")


def approve_tour(db: Session, tour_id: uuid.UUID) -> Tour:
    return update_tour_status(db, tour_id, "APPROVED")


def complete_tour(db: Session, tour_id: uuid.UUID) -> Tour:
    return update_tour_status(db, tour_id, "COMPLETED")






