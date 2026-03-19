from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select

from src.core.dependencies import CurrentUserID, DBSession, http_bearer
from src.crud.crud_provider import crud_provider
from src.models.listing import Listing
from src.models.tour import Tour

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(http_bearer)],
)


@router.get("/summary")
def get_dashboard_summary(db: DBSession, user_id: CurrentUserID):
    # Find provider for current user
    provider = crud_provider.get_by_user_id(db, uuid.UUID(user_id))
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found for this user",
        )

    # Total listings for this provider
    total_listings = db.execute(
        select(func.count(Listing.id)).where(Listing.provider_id == provider.id)
    ).scalar_one()

    # Active listings for this provider (status = 'ACTIVE')
    active_listings = db.execute(
        select(func.count(Listing.id)).where(
            Listing.provider_id == provider.id, Listing.status == "ACTIVE"
        )
    ).scalar_one()

    # Pending review listings for this provider (status = 'PENDING')
    pending_review_listings = db.execute(
        select(func.count(Listing.id)).where(
            Listing.provider_id == provider.id, Listing.status == "PENDING"
        )
    ).scalar_one()

    # Total tours for this provider (join tours -> listings)
    total_tours = db.execute(
        select(func.count(Tour.id)).join(Listing, Tour.listing_id == Listing.id).where(
            Listing.provider_id == provider.id
        )
    ).scalar_one()

    return {
        "total_listings": total_listings,
        "active_listings": active_listings,
        "pending_review": pending_review_listings,
        "total_tours": total_tours,
    }

