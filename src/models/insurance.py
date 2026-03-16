from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.session import Base

if TYPE_CHECKING:
    from src.models.listing import Listing


class InsuranceOption(Base):
    __tablename__ = "insurance_options"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ── Relationships ─────────────────────────────────────────────────────
    listing_insurance_options: Mapped[List["ListingInsuranceOption"]] = relationship(
        "ListingInsuranceOption",
        back_populates="insurance_option",
        cascade="all, delete-orphan",
    )


class ListingInsuranceOption(Base):
    __tablename__ = "listing_insurance_options"
    __table_args__ = (
        UniqueConstraint("listing_id", "insurance_option_id", name="uq_listing_insurance"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    listing_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("listings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    insurance_option_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("insurance_options.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ── Relationships ─────────────────────────────────────────────────────
    listing: Mapped["Listing"] = relationship(
        "Listing", back_populates="listing_insurance_options"
    )
    insurance_option: Mapped["InsuranceOption"] = relationship(
        "InsuranceOption", back_populates="listing_insurance_options"
    )






