from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.session import Base

if TYPE_CHECKING:
    from src.models.provider import Provider
    from src.models.listing_image import ListingImage
    from src.models.amenity import ListingAmenity
    from src.models.service import ListingService
    from src.models.equipment import ListingEquipment
    from src.models.language import ListingLanguage
    from src.models.certification import ListingCertification
    from src.models.activity import ListingActivity
    from src.models.dining import ListingDiningOption
    from src.models.safety import ListingSafetyFeature
    from src.models.insurance import ListingInsuranceOption
    from src.models.house_rule import ListingHouseRule
    from src.models.tour import Tour
    from src.models.review import Review
    from src.models.favorite import Favorite
    from src.models.report import Report


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    provider_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("providers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    care_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # ASSISTED_LIVING | MEMORY_CARE | INDEPENDENT_LIVING | ADULT_FAMILY_HOME | SKILLED_NURSING
    room_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # PRIVATE | SEMI_PRIVATE | SHARED
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(11, 8), nullable=True)
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    available_beds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    staff_ratio: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    established_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    license_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_24_hour_care: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="PENDING"
    )  # ACTIVE | INACTIVE | PENDING | SUSPENDED
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ── Relationships ─────────────────────────────────────────────────────
    provider: Mapped["Provider"] = relationship("Provider", back_populates="listings")
    images: Mapped[List["ListingImage"]] = relationship(
        "ListingImage", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_amenities: Mapped[List["ListingAmenity"]] = relationship(
        "ListingAmenity", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_services: Mapped[List["ListingService"]] = relationship(
        "ListingService", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_equipment: Mapped[List["ListingEquipment"]] = relationship(
        "ListingEquipment", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_languages: Mapped[List["ListingLanguage"]] = relationship(
        "ListingLanguage", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_certifications: Mapped[List["ListingCertification"]] = relationship(
        "ListingCertification", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_activities: Mapped[List["ListingActivity"]] = relationship(
        "ListingActivity", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_dining_options: Mapped[List["ListingDiningOption"]] = relationship(
        "ListingDiningOption", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_safety_features: Mapped[List["ListingSafetyFeature"]] = relationship(
        "ListingSafetyFeature", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_insurance_options: Mapped[List["ListingInsuranceOption"]] = relationship(
        "ListingInsuranceOption", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_house_rules: Mapped[List["ListingHouseRule"]] = relationship(
        "ListingHouseRule", back_populates="listing", cascade="all, delete-orphan"
    )
    tours: Mapped[List["Tour"]] = relationship(
        "Tour", back_populates="listing", cascade="all, delete-orphan"
    )
    reviews: Mapped[List["Review"]] = relationship(
        "Review", back_populates="listing", cascade="all, delete-orphan"
    )
    favorites: Mapped[List["Favorite"]] = relationship(
        "Favorite", back_populates="listing", cascade="all, delete-orphan"
    )
    reports: Mapped[List["Report"]] = relationship(
        "Report", back_populates="listing"
    )





