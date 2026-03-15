from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.crud.crud_provider import crud_provider
from src.models.provider import Provider
from src.schemas.provider import ProviderCreate, ProviderUpdate


def register_provider(db: Session, payload: ProviderCreate) -> Provider:
    """Create a new provider profile.

    Raises 400 if the user already has a provider profile.
    """
    existing = crud_provider.get_by_user_id(db, payload.user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a provider profile",
        )
    return crud_provider.create(db, payload)


def verify_provider(db: Session, provider_id: uuid.UUID) -> Provider:
    """Mark a provider as VERIFIED (admin action)."""
    provider = crud_provider.get_by_id(db, provider_id)
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    provider.verification_status = "VERIFIED"
    provider.verified_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(provider)
    return provider


def reject_provider(db: Session, provider_id: uuid.UUID) -> Provider:
    """Mark a provider as REJECTED (admin action)."""
    provider = crud_provider.get_by_id(db, provider_id)
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    provider.verification_status = "REJECTED"
    db.commit()
    db.refresh(provider)
    return provider


def update_provider(
    db: Session, provider_id: uuid.UUID, payload: ProviderUpdate
) -> Provider:
    provider = crud_provider.get_by_id(db, provider_id)
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return crud_provider.update(db, provider, payload)


