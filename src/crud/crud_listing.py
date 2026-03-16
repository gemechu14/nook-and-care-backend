from __future__ import annotations

import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.crud.base import CRUDBase
from src.models.listing import Listing
from src.models.amenity import ListingAmenity
from src.models.language import ListingLanguage
from src.models.certification import ListingCertification
from src.models.activity import ListingActivity
from src.models.dining import ListingDiningOption
from src.models.safety import ListingSafetyFeature
from src.models.insurance import ListingInsuranceOption
from src.models.house_rule import ListingHouseRule
from src.models.equipment import ListingEquipment
from src.models.service import ListingService
from src.schemas.listing import ListingCreate, ListingUpdate


class CRUDListing(CRUDBase[Listing, ListingCreate, ListingUpdate]):

    def get_by_id(self, db: Session, record_id: uuid.UUID) -> Optional[Listing]:
        """Return a single listing by primary key with all relationships eagerly loaded."""
        stmt = (
            select(Listing)
            .where(Listing.id == record_id)
            .options(
                selectinload(Listing.images),
                selectinload(Listing.listing_amenities).selectinload(ListingAmenity.amenity),
                selectinload(Listing.listing_languages).selectinload(ListingLanguage.language),
                selectinload(Listing.listing_certifications).selectinload(ListingCertification.certification),
                selectinload(Listing.listing_activities).selectinload(ListingActivity.activity),
                selectinload(Listing.listing_dining_options).selectinload(ListingDiningOption.dining_option),
                selectinload(Listing.listing_safety_features).selectinload(ListingSafetyFeature.safety_feature),
                selectinload(Listing.listing_insurance_options).selectinload(ListingInsuranceOption.insurance_option),
                selectinload(Listing.listing_house_rules).selectinload(ListingHouseRule.house_rule),
                selectinload(Listing.listing_equipment).selectinload(ListingEquipment.equipment),
                selectinload(Listing.listing_services).selectinload(ListingService.treatment_service),
            )
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_by_provider(
        self, db: Session, provider_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .where(Listing.provider_id == provider_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_active(self, db: Session, skip: int = 0, limit: int = 20) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .where(Listing.status == "ACTIVE")
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def get_featured(
        self, db: Session, skip: int = 0, limit: int = 20, status: Optional[str] = None
    ) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .where(Listing.is_featured.is_(True))
            .options(
                selectinload(Listing.images),
                selectinload(Listing.listing_amenities).selectinload(ListingAmenity.amenity),
                selectinload(Listing.listing_languages).selectinload(ListingLanguage.language),
                selectinload(Listing.listing_certifications).selectinload(ListingCertification.certification),
                selectinload(Listing.listing_activities).selectinload(ListingActivity.activity),
                selectinload(Listing.listing_dining_options).selectinload(ListingDiningOption.dining_option),
                selectinload(Listing.listing_safety_features).selectinload(ListingSafetyFeature.safety_feature),
                selectinload(Listing.listing_insurance_options).selectinload(ListingInsuranceOption.insurance_option),
                selectinload(Listing.listing_house_rules).selectinload(ListingHouseRule.house_rule),
                selectinload(Listing.listing_equipment).selectinload(ListingEquipment.equipment),
                selectinload(Listing.listing_services).selectinload(ListingService.treatment_service),
            )
        )
        
        # Filter by status if provided, otherwise default to ACTIVE (backward compatibility)
        if status:
            stmt = stmt.where(Listing.status == status)
        else:
            stmt = stmt.where(Listing.status == "ACTIVE")
        
        stmt = stmt.offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def search(
        self,
        db: Session,
        city: Optional[str] = None,
        care_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .options(selectinload(Listing.images))
        )
        
        if city:
            stmt = stmt.where(Listing.city.ilike(f"%{city}%"))
        if care_type:
            stmt = stmt.where(Listing.care_type == care_type)
        if min_price is not None:
            stmt = stmt.where(Listing.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Listing.price <= max_price)
        if status:
            stmt = stmt.where(Listing.status == status)
        stmt = stmt.offset(skip).limit(limit)
        
        return db.execute(stmt).scalars().all()


crud_listing = CRUDListing(Listing)





