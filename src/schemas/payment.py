from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    provider_id: uuid.UUID
    amount: float
    currency: str = "USD"
    payment_method: str  # CREDIT_CARD | PAYPAL | BANK_TRANSFER
    transaction_id: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    transaction_id: Optional[str] = None
    processed_at: Optional[datetime] = None


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    processed_at: Optional[datetime] = None
    created_at: datetime






