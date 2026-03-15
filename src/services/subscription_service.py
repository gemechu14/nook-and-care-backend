from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.crud.crud_subscription import crud_subscription
from src.models.subscription import Subscription
from src.schemas.subscription import SubscriptionCreate

# Plan listing limits (None = unlimited)
PLAN_LISTING_LIMITS: dict[str, int | None] = {
    "FREE": 1,
    "PRO": None,
    "PREMIUM": None,
}


def subscribe(db: Session, payload: SubscriptionCreate) -> Subscription:
    """Create a subscription for a provider.

    Cancels any existing ACTIVE subscription before creating a new one.
    """
    existing = crud_subscription.get_active_by_provider(db, payload.provider_id)
    if existing:
        existing.status = "CANCELLED"
        db.commit()

    return crud_subscription.create(db, payload)


def cancel_subscription(db: Session, subscription_id: uuid.UUID) -> Subscription:
    sub = crud_subscription.get_by_id(db, subscription_id)
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    if sub.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscription is not active",
        )
    sub.status = "CANCELLED"
    db.commit()
    db.refresh(sub)
    return sub


def check_listing_limit(db: Session, provider_id: uuid.UUID, current_listing_count: int) -> None:
    """Raise 403 if the provider has exceeded their plan's listing limit."""
    from src.crud.crud_listing import crud_listing

    active_sub = crud_subscription.get_active_by_provider(db, provider_id)
    plan = active_sub.plan_type if active_sub else "FREE"
    limit = PLAN_LISTING_LIMITS.get(plan)
    if limit is not None and current_listing_count >= limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Your {plan} plan allows a maximum of {limit} listing(s). "
            "Upgrade your subscription to add more.",
        )





