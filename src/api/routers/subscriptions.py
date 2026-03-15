from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.core.dependencies import DBSession, PaginationParams
from src.crud.crud_subscription import crud_subscription
from src.schemas.subscription import SubscriptionCreate, SubscriptionRead, SubscriptionUpdate
from src.services import subscription_service

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.get("/", response_model=List[SubscriptionRead])
def list_subscriptions(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_subscription.get_all(db, skip=skip, limit=limit)


@router.get("/{subscription_id}", response_model=SubscriptionRead)
def get_subscription(subscription_id: uuid.UUID, db: DBSession):
    sub = crud_subscription.get_by_id(db, subscription_id)
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    return sub


@router.post("/", response_model=SubscriptionRead, status_code=201)
def create_subscription(payload: SubscriptionCreate, db: DBSession):
    return subscription_service.subscribe(db, payload)


@router.put("/{subscription_id}", response_model=SubscriptionRead)
def update_subscription(
    subscription_id: uuid.UUID, payload: SubscriptionUpdate, db: DBSession
):
    sub = crud_subscription.get_by_id(db, subscription_id)
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )
    return crud_subscription.update(db, sub, payload)


@router.post("/{subscription_id}/cancel", response_model=SubscriptionRead)
def cancel_subscription(subscription_id: uuid.UUID, db: DBSession):
    return subscription_service.cancel_subscription(db, subscription_id)


