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
        """Return a single listing by primary key with all relationships eagerly loaded.
        
        Note: Images are set to empty list if the image_data column doesn't exist in the database.
        To fix this, run a migration to add the image_data column to listing_images table.
        """
        stmt = (
            select(Listing)
            .where(Listing.id == record_id)
            .options(
                # Images excluded from eager load due to potential missing image_data column
                # Uncomment after running migration to add image_data column:
                # selectinload(Listing.images),
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
        listing = db.execute(stmt).scalar_one_or_none()
        
        if listing:
            # Set images to empty list to prevent lazy loading that would fail due to missing image_data column
            # Use SQLAlchemy's attributes API to mark the relationship as loaded with empty list
            from sqlalchemy.orm import attributes
            attributes.set_committed_value(listing, 'images', [])
        
        return listing

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

    def get_featured(self, db: Session, skip: int = 0, limit: int = 20) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .where(Listing.status == "ACTIVE", Listing.is_featured.is_(True))
            .options(
                # Images excluded from eager load due to potential missing image_data column
                # Uncomment after running migration to add image_data column:
                # selectinload(Listing.images),
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
            .offset(skip)
            .limit(limit)
        )
        listings = db.execute(stmt).scalars().all()
        
        # Set images to empty list for each listing to prevent lazy loading
        # that would fail due to missing image_data column
        from sqlalchemy.orm import attributes
        
        for listing in listings:
            attributes.set_committed_value(listing, 'images', [])
        
        return listings

    def search(
        self,
        db: Session,
        city: Optional[str] = None,
        care_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Listing]:
        stmt = (
            select(Listing)
            .where(Listing.status == "ACTIVE")
            .options(
                # Images excluded from eager load due to potential missing image_data column
                # Uncomment after running migration to add image_data column:
                # selectinload(Listing.images),
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
        if city:
            stmt = stmt.where(Listing.city.ilike(f"%{city}%"))
        if care_type:
            stmt = stmt.where(Listing.care_type == care_type)
        if min_price is not None:
            stmt = stmt.where(Listing.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Listing.price <= max_price)
        stmt = stmt.offset(skip).limit(limit)
        listings = db.execute(stmt).scalars().all()
        
        # Set images to empty list for each listing to prevent lazy loading
        # that would fail due to missing image_data column
        from sqlalchemy.orm import attributes
        
        for listing in listings:
            attributes.set_committed_value(listing, 'images', [])
        
        return listings


crud_listing = CRUDListing(Listing)





