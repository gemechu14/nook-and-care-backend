from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.core.dependencies import DBSession, PaginationParams
from src.crud.crud_tour import crud_tour
from src.schemas.tour import TourCreate, TourRead, TourUpdate
from src.services import tour_service

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.get("/", response_model=List[TourRead])
def list_tours(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_tour.get_all(db, skip=skip, limit=limit)


@router.get("/{tour_id}", response_model=TourRead)
def get_tour(tour_id: uuid.UUID, db: DBSession):
    tour = crud_tour.get_by_id(db, tour_id)
    if tour is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tour not found")
    return tour


@router.post("/", response_model=TourRead, status_code=201)
def book_tour(payload: TourCreate, db: DBSession):
    """Book a tour for a listing."""
    return tour_service.book_tour(db, payload)


@router.put("/{tour_id}", response_model=TourRead)
def update_tour(tour_id: uuid.UUID, payload: TourUpdate, db: DBSession):
    tour = crud_tour.get_by_id(db, tour_id)
    if tour is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tour not found")
    return crud_tour.update(db, tour, payload)


@router.post("/{tour_id}/approve", response_model=TourRead)
def approve_tour(tour_id: uuid.UUID, db: DBSession):
    return tour_service.approve_tour(db, tour_id)


@router.post("/{tour_id}/cancel", response_model=TourRead)
def cancel_tour(tour_id: uuid.UUID, db: DBSession):
    return tour_service.cancel_tour(db, tour_id)


@router.post("/{tour_id}/complete", response_model=TourRead)
def complete_tour(tour_id: uuid.UUID, db: DBSession):
    return tour_service.complete_tour(db, tour_id)


@router.delete("/{tour_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tour(tour_id: uuid.UUID, db: DBSession):
    deleted = crud_tour.delete(db, tour_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tour not found")


