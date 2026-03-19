from __future__ import annotations

from datetime import datetime, timedelta, timezone
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select

from src.core.dependencies import CurrentUserID, DBSession, http_bearer, require_role
from src.crud.crud_provider import crud_provider
from src.models.listing import Listing
from src.models.provider import Provider
from src.models.report import Report
from src.models.tour import Tour

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(http_bearer)],
)


def _trend(current_week_count: int, previous_week_count: int) -> dict:
    delta = current_week_count - previous_week_count
    if previous_week_count == 0:
        percent_change = 100.0 if current_week_count > 0 else 0.0
    else:
        percent_change = (delta / previous_week_count) * 100.0

    if delta > 0:
        direction = "up"
        delta_label = f"+{delta}"
        percent_label = f"\u2191 +{abs(percent_change):.1f}%"
    elif delta < 0:
        direction = "down"
        delta_label = f"{delta}"
        percent_label = f"\u2193 -{abs(percent_change):.1f}%"
    else:
        direction = "flat"
        delta_label = "0"
        percent_label = "\u2192 0.0%"

    return {
        "this_week": current_week_count,
        "previous_week": previous_week_count,
        "delta": delta,
        "delta_label": delta_label,
        "percent_change": round(percent_change, 1),
        "percent_label": percent_label,
        "direction": direction,
    }


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


@router.get("/admin/summary")
def get_admin_dashboard_summary(
    db: DBSession,
    _: None = Depends(require_role("ADMIN")),
):
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=7)
    prev_week_start = week_start - timedelta(days=7)

    total_providers = db.execute(select(func.count(Provider.id))).scalar_one()
    pending_providers = db.execute(
        select(func.count(Provider.id)).where(Provider.verification_status == "PENDING")
    ).scalar_one()
    active_providers = db.execute(
        select(func.count(Provider.id)).where(Provider.verification_status == "VERIFIED")
    ).scalar_one()
    total_active_listings = db.execute(
        select(func.count(Listing.id)).where(Listing.status == "ACTIVE")
    ).scalar_one()
    total_reports = db.execute(select(func.count(Report.id))).scalar_one()

    providers_this_week = db.execute(
        select(func.count(Provider.id)).where(Provider.created_at >= week_start)
    ).scalar_one()
    providers_prev_week = db.execute(
        select(func.count(Provider.id)).where(
            Provider.created_at >= prev_week_start,
            Provider.created_at < week_start,
        )
    ).scalar_one()

    active_listings_this_week = db.execute(
        select(func.count(Listing.id)).where(
            Listing.status == "ACTIVE",
            Listing.created_at >= week_start,
        )
    ).scalar_one()
    active_listings_prev_week = db.execute(
        select(func.count(Listing.id)).where(
            Listing.status == "ACTIVE",
            Listing.created_at >= prev_week_start,
            Listing.created_at < week_start,
        )
    ).scalar_one()

    reports_this_week = db.execute(
        select(func.count(Report.id)).where(Report.created_at >= week_start)
    ).scalar_one()
    reports_prev_week = db.execute(
        select(func.count(Report.id)).where(
            Report.created_at >= prev_week_start,
            Report.created_at < week_start,
        )
    ).scalar_one()

    return {
        "total_providers": total_providers,
        "pending_providers": pending_providers,
        "active_providers": active_providers,
        "total_active_listings": total_active_listings,
        "total_reports": total_reports,
        "trends": {
            "total_providers": _trend(providers_this_week, providers_prev_week),
            "total_active_listings": _trend(active_listings_this_week, active_listings_prev_week),
            "total_reports": _trend(reports_this_week, reports_prev_week),
        },
    }

