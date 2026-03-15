from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import DBSession, PaginationParams, http_bearer
from src.crud.crud_review import crud_review
from src.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", response_model=List[ReviewRead])
def list_reviews(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_review.get_all(db, skip=skip, limit=limit)


@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: uuid.UUID, db: DBSession):
    review = crud_review.get_by_id(db, review_id)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@router.post("/", response_model=ReviewRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_review(payload: ReviewCreate, db: DBSession):
    return crud_review.create(db, payload)


@router.put("/{review_id}", response_model=ReviewRead, dependencies=[Depends(http_bearer)])
def update_review(review_id: uuid.UUID, payload: ReviewUpdate, db: DBSession):
    review = crud_review.get_by_id(db, review_id)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return crud_review.update(db, review, payload)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(http_bearer)])
def delete_review(review_id: uuid.UUID, db: DBSession):
    deleted = crud_review.delete(db, review_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")


