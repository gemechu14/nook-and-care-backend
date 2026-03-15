from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.core.dependencies import DBSession, PaginationParams
from src.crud.crud_payment import crud_payment
from src.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=List[PaymentRead])
def list_payments(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_payment.get_all(db, skip=skip, limit=limit)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: uuid.UUID, db: DBSession):
    payment = crud_payment.get_by_id(db, payment_id)
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


@router.post("/", response_model=PaymentRead, status_code=201)
def create_payment(payload: PaymentCreate, db: DBSession):
    return crud_payment.create(db, payload)


@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: uuid.UUID, payload: PaymentUpdate, db: DBSession):
    payment = crud_payment.get_by_id(db, payment_id)
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return crud_payment.update(db, payment, payload)


