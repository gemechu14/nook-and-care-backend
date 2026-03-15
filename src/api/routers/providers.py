from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import DBSession, PaginationParams, http_bearer
from src.crud.crud_provider import crud_provider
from src.schemas.provider import ProviderCreate, ProviderRead, ProviderUpdate
from src.services import provider_service

router = APIRouter(
    prefix="/providers",
    tags=["Providers"],
    dependencies=[Depends(http_bearer)],
)


@router.get("/", response_model=List[ProviderRead])
def list_providers(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_provider.get_all(db, skip=skip, limit=limit)


@router.get("/{provider_id}", response_model=ProviderRead)
def get_provider(provider_id: uuid.UUID, db: DBSession):
    provider = crud_provider.get_by_id(db, provider_id)
    if provider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return provider


@router.post("/", response_model=ProviderRead, status_code=201)
def create_provider(payload: ProviderCreate, db: DBSession):
    return provider_service.register_provider(db, payload)


@router.put("/{provider_id}", response_model=ProviderRead)
def update_provider(provider_id: uuid.UUID, payload: ProviderUpdate, db: DBSession):
    return provider_service.update_provider(db, provider_id, payload)


@router.post("/{provider_id}/verify", response_model=ProviderRead)
def verify_provider(provider_id: uuid.UUID, db: DBSession):
    """Admin: verify a provider."""
    return provider_service.verify_provider(db, provider_id)


@router.post("/{provider_id}/reject", response_model=ProviderRead)
def reject_provider(provider_id: uuid.UUID, db: DBSession):
    """Admin: reject a provider."""
    return provider_service.reject_provider(db, provider_id)


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider(provider_id: uuid.UUID, db: DBSession):
    deleted = crud_provider.delete(db, provider_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")


