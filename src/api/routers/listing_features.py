"""Batch operations for listing features (amenities, activities, languages, etc.)."""
from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.dependencies import CurrentUserID, DBSession, http_bearer
from src.crud.crud_amenity import crud_listing_amenity
from src.crud.crud_activity import crud_listing_activity
from src.crud.crud_language import crud_listing_language
from src.crud.crud_certification import crud_listing_certification
from src.crud.crud_dining import crud_listing_dining_option
from src.crud.crud_safety import crud_listing_safety_feature
from src.crud.crud_insurance import crud_listing_insurance_option
from src.crud.crud_house_rule import crud_listing_house_rule
from src.crud.crud_equipment import crud_listing_equipment
from src.crud.crud_service import crud_listing_service
from src.crud.crud_listing import crud_listing
from src.crud.crud_provider import crud_provider
from src.crud.crud_user import get_by_id as get_user
from src.schemas.amenity import (
    ListingAmenityBatchCreate,
    ListingAmenityBatchDelete,
    ListingAmenityRead,
)
from src.schemas.activity import (
    ListingActivityBatchCreate,
    ListingActivityBatchDelete,
    ListingActivityRead,
)
from src.schemas.language import (
    ListingLanguageBatchCreate,
    ListingLanguageBatchDelete,
    ListingLanguageRead,
)
from src.schemas.certification import (
    ListingCertificationBatchCreate,
    ListingCertificationBatchDelete,
    ListingCertificationRead,
)
from src.schemas.dining import (
    ListingDiningOptionBatchCreate,
    ListingDiningOptionBatchDelete,
    ListingDiningOptionRead,
)
from src.schemas.safety import (
    ListingSafetyFeatureBatchCreate,
    ListingSafetyFeatureBatchDelete,
    ListingSafetyFeatureRead,
)
from src.schemas.insurance import (
    ListingInsuranceOptionBatchCreate,
    ListingInsuranceOptionBatchDelete,
    ListingInsuranceOptionRead,
)
from src.schemas.house_rule import (
    ListingHouseRuleBatchCreate,
    ListingHouseRuleBatchDelete,
    ListingHouseRuleRead,
)
from src.schemas.equipment import (
    ListingEquipmentBatchCreate,
    ListingEquipmentBatchDelete,
    ListingEquipmentRead,
)
from src.schemas.service import (
    ListingServiceBatchCreate,
    ListingServiceBatchDelete,
    ListingServiceRead,
)

router = APIRouter(tags=["Listing Features – Batch Operations"])


# ── Helper Functions ────────────────────────────────────────────────────────────

def verify_provider_owns_listing(
    db: Session, user_id: str, listing_id: uuid.UUID
) -> None:
    """Verify that the authenticated user (as a provider) owns the listing.
    
    Raises 403 if user is not a provider or doesn't own the listing.
    Raises 404 if listing doesn't exist.
    """
    user = get_user(db, user_id)
    if user is None or user.role not in ("PROVIDER", "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only providers and admins can manage listing features",
        )
    
    if user.role == "ADMIN":
        # Admins can manage any listing
        listing = crud_listing.get_by_id(db, listing_id)
        if listing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found",
            )
        return
    
    # For providers, verify ownership
    provider = crud_provider.get_by_user_id(db, uuid.UUID(user_id))
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Provider profile not found",
        )
    
    listing = crud_listing.get_by_id(db, listing_id)
    if listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    
    if listing.provider_id != provider.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage this listing",
        )


def verify_all_listings_same(
    db: Session, user_id: str, listing_ids: list[uuid.UUID]
) -> uuid.UUID:
    """Verify all listing IDs are the same and user owns it.
    
    Returns the listing_id if valid.
    Raises 400 if listing IDs differ.
    """
    if not listing_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No items provided",
        )
    
    # Check all listing IDs are the same
    first_listing_id = listing_ids[0]
    if not all(lid == first_listing_id for lid in listing_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All items must reference the same listing",
        )
    
    # Verify ownership
    verify_provider_owns_listing(db, user_id, first_listing_id)
    return first_listing_id


# ── Listing Amenities ───────────────────────────────────────────────────────────

@router.post(
    "/listing-amenities/batch",
    response_model=List[ListingAmenityRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing amenities",
    description="Create multiple amenity associations for a listing in a single request. All items must reference the same listing.",
    response_description="List of created listing amenity associations",
)
def batch_create_listing_amenities(
    payload: ListingAmenityBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing amenities.
    
    - Requires authentication (Bearer token)
    - User must be a provider who owns the listing, or an admin
    - All items must reference the same listing
    - Prevents duplicate associations
    - Validates all amenity IDs exist
    """
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    # Validate all amenity IDs exist
    from src.crud.crud_amenity import crud_amenity
    amenity_ids = {item.amenity_id for item in payload.items}
    for amenity_id in amenity_ids:
        if crud_amenity.get_by_id(db, amenity_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Amenity {amenity_id} not found",
            )
    
    # Check for duplicates
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.amenity_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + amenity {item.amenity_id}",
            )
        seen.add(key)
    
    # Check existing associations
    from src.models.amenity import ListingAmenity
    existing_stmt = select(ListingAmenity).where(
        ListingAmenity.listing_id == listing_ids[0],
        ListingAmenity.amenity_id.in_(amenity_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_amenity_ids = {e.amenity_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some amenities already associated: {existing_amenity_ids}",
        )
    
    # Create all items
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_amenity.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create amenities: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-amenities/batch",
    response_model=List[ListingAmenityRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing amenities",
    description="Delete multiple amenity associations for a listing in a single request. All items must reference the same listing.",
    response_description="List of deleted listing amenity associations",
)
def batch_delete_listing_amenities(
    payload: ListingAmenityBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing amenities.
    
    - Requires authentication (Bearer token)
    - User must be a provider who owns the listing, or an admin
    - All items must reference the same listing
    - Returns only successfully deleted items
    """
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.amenity import ListingAmenity
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingAmenity).where(
                ListingAmenity.listing_id == item.listing_id,
                ListingAmenity.amenity_id == item.amenity_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete amenities: {str(e)}",
        )
    
    return deleted


# ── Listing Activities ──────────────────────────────────────────────────────────

@router.post(
    "/listing-activities/batch",
    response_model=List[ListingActivityRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing activities",
    description="Create multiple activity associations for a listing in a single request.",
    response_description="List of created listing activity associations",
)
def batch_create_listing_activities(
    payload: ListingActivityBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing activities."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_activity import crud_activity
    activity_ids = {item.activity_id for item in payload.items}
    for activity_id in activity_ids:
        if crud_activity.get_by_id(db, activity_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Activity {activity_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.activity_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + activity {item.activity_id}",
            )
        seen.add(key)
    
    from src.models.activity import ListingActivity
    existing_stmt = select(ListingActivity).where(
        ListingActivity.listing_id == listing_ids[0],
        ListingActivity.activity_id.in_(activity_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_activity_ids = {e.activity_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some activities already associated: {existing_activity_ids}",
        )
    
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_activity.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create activities: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-activities/batch",
    response_model=List[ListingActivityRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing activities",
    description="Delete multiple activity associations for a listing in a single request.",
    response_description="List of deleted listing activity associations",
)
def batch_delete_listing_activities(
    payload: ListingActivityBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing activities."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.activity import ListingActivity
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingActivity).where(
                ListingActivity.listing_id == item.listing_id,
                ListingActivity.activity_id == item.activity_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete activities: {str(e)}",
        )
    
    return deleted


# ── Listing Languages ───────────────────────────────────────────────────────────

@router.post(
    "/listing-languages/batch",
    response_model=List[ListingLanguageRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing languages",
    description="Create multiple language associations for a listing in a single request.",
    response_description="List of created listing language associations",
)
def batch_create_listing_languages(
    payload: ListingLanguageBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing languages."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_language import crud_language
    language_ids = {item.language_id for item in payload.items}
    for language_id in language_ids:
        if crud_language.get_by_id(db, language_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Language {language_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.language_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + language {item.language_id}",
            )
        seen.add(key)
    
    from src.models.language import ListingLanguage
    existing_stmt = select(ListingLanguage).where(
        ListingLanguage.listing_id == listing_ids[0],
        ListingLanguage.language_id.in_(language_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_language_ids = {e.language_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some languages already associated: {existing_language_ids}",
        )
    
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_language.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create languages: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-languages/batch",
    response_model=List[ListingLanguageRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing languages",
    description="Delete multiple language associations for a listing in a single request.",
    response_description="List of deleted listing language associations",
)
def batch_delete_listing_languages(
    payload: ListingLanguageBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing languages."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.language import ListingLanguage
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingLanguage).where(
                ListingLanguage.listing_id == item.listing_id,
                ListingLanguage.language_id == item.language_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete languages: {str(e)}",
        )
    
    return deleted


# ── Listing Certifications ──────────────────────────────────────────────────────

@router.post(
    "/listing-certifications/batch",
    response_model=List[ListingCertificationRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing certifications",
    description="Create multiple certification associations for a listing in a single request. Supports optional license_number field.",
    response_description="List of created listing certification associations",
)
def batch_create_listing_certifications(
    payload: ListingCertificationBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing certifications."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_certification import crud_certification
    certification_ids = {item.certification_id for item in payload.items}
    for certification_id in certification_ids:
        if crud_certification.get_by_id(db, certification_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Certification {certification_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.certification_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + certification {item.certification_id}",
            )
        seen.add(key)
    
    from src.models.certification import ListingCertification
    existing_stmt = select(ListingCertification).where(
        ListingCertification.listing_id == listing_ids[0],
        ListingCertification.certification_id.in_(certification_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_certification_ids = {e.certification_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some certifications already associated: {existing_certification_ids}",
        )
    
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_certification.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create certifications: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-certifications/batch",
    response_model=List[ListingCertificationRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing certifications",
    description="Delete multiple certification associations for a listing in a single request.",
    response_description="List of deleted listing certification associations",
)
def batch_delete_listing_certifications(
    payload: ListingCertificationBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing certifications."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.certification import ListingCertification
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingCertification).where(
                ListingCertification.listing_id == item.listing_id,
                ListingCertification.certification_id == item.certification_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete certifications: {str(e)}",
        )
    
    return deleted


# ── Listing Dining Options ──────────────────────────────────────────────────────

@router.post(
    "/listing-dining-options/batch",
    response_model=List[ListingDiningOptionRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing dining options",
    description="Create multiple dining option associations for a listing in a single request.",
    response_description="List of created listing dining option associations",
)
def batch_create_listing_dining_options(
    payload: ListingDiningOptionBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing dining options."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_dining import crud_dining_option
    dining_option_ids = {item.dining_option_id for item in payload.items}
    for dining_option_id in dining_option_ids:
        if crud_dining_option.get_by_id(db, dining_option_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dining option {dining_option_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.dining_option_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + dining_option {item.dining_option_id}",
            )
        seen.add(key)
    
    from src.models.dining import ListingDiningOption
    existing_stmt = select(ListingDiningOption).where(
        ListingDiningOption.listing_id == listing_ids[0],
        ListingDiningOption.dining_option_id.in_(dining_option_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_dining_option_ids = {e.dining_option_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some dining options already associated: {existing_dining_option_ids}",
        )
    
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_dining_option.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create dining options: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-dining-options/batch",
    response_model=List[ListingDiningOptionRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing dining options",
    description="Delete multiple dining option associations for a listing in a single request.",
    response_description="List of deleted listing dining option associations",
)
def batch_delete_listing_dining_options(
    payload: ListingDiningOptionBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing dining options."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.dining import ListingDiningOption
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingDiningOption).where(
                ListingDiningOption.listing_id == item.listing_id,
                ListingDiningOption.dining_option_id == item.dining_option_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete dining options: {str(e)}",
        )
    
    return deleted


# ── Listing Safety Features ──────────────────────────────────────────────────────

@router.post(
    "/listing-safety-features/batch",
    response_model=List[ListingSafetyFeatureRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing safety features",
    description="Create multiple safety feature associations for a listing in a single request.",
    response_description="List of created listing safety feature associations",
)
def batch_create_listing_safety_features(
    payload: ListingSafetyFeatureBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing safety features."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_safety import crud_safety_feature
    safety_feature_ids = {item.safety_feature_id for item in payload.items}
    for safety_feature_id in safety_feature_ids:
        if crud_safety_feature.get_by_id(db, safety_feature_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Safety feature {safety_feature_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.safety_feature_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + safety_feature {item.safety_feature_id}",
            )
        seen.add(key)
    
    from src.models.safety import ListingSafetyFeature
    existing_stmt = select(ListingSafetyFeature).where(
        ListingSafetyFeature.listing_id == listing_ids[0],
        ListingSafetyFeature.safety_feature_id.in_(safety_feature_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_safety_feature_ids = {e.safety_feature_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some safety features already associated: {existing_safety_feature_ids}",
        )
    
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_safety_feature.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create safety features: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-safety-features/batch",
    response_model=List[ListingSafetyFeatureRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing safety features",
    description="Delete multiple safety feature associations for a listing in a single request.",
    response_description="List of deleted listing safety feature associations",
)
def batch_delete_listing_safety_features(
    payload: ListingSafetyFeatureBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing safety features."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.safety import ListingSafetyFeature
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingSafetyFeature).where(
                ListingSafetyFeature.listing_id == item.listing_id,
                ListingSafetyFeature.safety_feature_id == item.safety_feature_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete safety features: {str(e)}",
        )
    
    return deleted


# ── Listing Insurance Options ───────────────────────────────────────────────────

@router.post(
    "/listing-insurance-options/batch",
    response_model=List[ListingInsuranceOptionRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing insurance options",
    description="Create multiple insurance option associations for a listing in a single request.",
    response_description="List of created listing insurance option associations",
)
def batch_create_listing_insurance_options(
    payload: ListingInsuranceOptionBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing insurance options."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_insurance import crud_insurance_option
    insurance_option_ids = {item.insurance_option_id for item in payload.items}
    for insurance_option_id in insurance_option_ids:
        if crud_insurance_option.get_by_id(db, insurance_option_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insurance option {insurance_option_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.insurance_option_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + insurance_option {item.insurance_option_id}",
            )
        seen.add(key)
    
    from src.models.insurance import ListingInsuranceOption
    existing_stmt = select(ListingInsuranceOption).where(
        ListingInsuranceOption.listing_id == listing_ids[0],
        ListingInsuranceOption.insurance_option_id.in_(insurance_option_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_insurance_option_ids = {e.insurance_option_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some insurance options already associated: {existing_insurance_option_ids}",
        )
    
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_insurance_option.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create insurance options: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-insurance-options/batch",
    response_model=List[ListingInsuranceOptionRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing insurance options",
    description="Delete multiple insurance option associations for a listing in a single request.",
    response_description="List of deleted listing insurance option associations",
)
def batch_delete_listing_insurance_options(
    payload: ListingInsuranceOptionBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing insurance options."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.insurance import ListingInsuranceOption
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingInsuranceOption).where(
                ListingInsuranceOption.listing_id == item.listing_id,
                ListingInsuranceOption.insurance_option_id == item.insurance_option_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete insurance options: {str(e)}",
        )
    
    return deleted


# ── Listing House Rules ────────────────────────────────────────────────────────

@router.post(
    "/listing-house-rules/batch",
    response_model=List[ListingHouseRuleRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing house rules",
    description="Create multiple house rule associations for a listing in a single request. Display order is auto-incremented if not provided.",
    response_description="List of created listing house rule associations",
)
def batch_create_listing_house_rules(
    payload: ListingHouseRuleBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing house rules."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_house_rule import crud_house_rule
    house_rule_ids = {item.house_rule_id for item in payload.items}
    for house_rule_id in house_rule_ids:
        if crud_house_rule.get_by_id(db, house_rule_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"House rule {house_rule_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.house_rule_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + house_rule {item.house_rule_id}",
            )
        seen.add(key)
    
    from src.models.house_rule import ListingHouseRule
    existing_stmt = select(ListingHouseRule).where(
        ListingHouseRule.listing_id == listing_ids[0],
        ListingHouseRule.house_rule_id.in_(house_rule_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_house_rule_ids = {e.house_rule_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some house rules already associated: {existing_house_rule_ids}",
        )
    
    created = []
    try:
        # Auto-increment display_order if not provided
        for idx, item in enumerate(payload.items):
            from src.schemas.house_rule import ListingHouseRuleCreate
            item_data = item.model_dump()
            if item_data.get("display_order") is None:
                item_data["display_order"] = idx
            create_schema = ListingHouseRuleCreate(**item_data)
            obj = crud_listing_house_rule.create(db, create_schema)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create house rules: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-house-rules/batch",
    response_model=List[ListingHouseRuleRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing house rules",
    description="Delete multiple house rule associations for a listing in a single request.",
    response_description="List of deleted listing house rule associations",
)
def batch_delete_listing_house_rules(
    payload: ListingHouseRuleBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing house rules."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.house_rule import ListingHouseRule
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingHouseRule).where(
                ListingHouseRule.listing_id == item.listing_id,
                ListingHouseRule.house_rule_id == item.house_rule_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete house rules: {str(e)}",
        )
    
    return deleted


# ── Listing Equipment ──────────────────────────────────────────────────────────

@router.post(
    "/listing-equipment/batch",
    response_model=List[ListingEquipmentRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing equipment",
    description="Create multiple equipment associations for a listing in a single request. Quantity defaults to 1 if not provided.",
    response_description="List of created listing equipment associations",
)
def batch_create_listing_equipment(
    payload: ListingEquipmentBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing equipment."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_equipment import crud_equipment
    equipment_ids = {item.equipment_id for item in payload.items}
    for equipment_id in equipment_ids:
        if crud_equipment.get_by_id(db, equipment_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipment {equipment_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.equipment_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + equipment {item.equipment_id}",
            )
        seen.add(key)
    
    from src.models.equipment import ListingEquipment
    existing_stmt = select(ListingEquipment).where(
        ListingEquipment.listing_id == listing_ids[0],
        ListingEquipment.equipment_id.in_(equipment_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_equipment_ids = {e.equipment_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some equipment already associated: {existing_equipment_ids}",
        )
    
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_equipment.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create equipment: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-equipment/batch",
    response_model=List[ListingEquipmentRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing equipment",
    description="Delete multiple equipment associations for a listing in a single request.",
    response_description="List of deleted listing equipment associations",
)
def batch_delete_listing_equipment(
    payload: ListingEquipmentBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing equipment."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.equipment import ListingEquipment
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingEquipment).where(
                ListingEquipment.listing_id == item.listing_id,
                ListingEquipment.equipment_id == item.equipment_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete equipment: {str(e)}",
        )
    
    return deleted


# ── Listing Services ────────────────────────────────────────────────────────────

@router.post(
    "/listing-services/batch",
    response_model=List[ListingServiceRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(http_bearer)],
    summary="Batch create listing services",
    description="Create multiple treatment service associations for a listing in a single request. Price is optional, is_included defaults to false.",
    response_description="List of created listing service associations",
)
def batch_create_listing_services(
    payload: ListingServiceBatchCreate,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch create listing services."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.crud.crud_service import crud_treatment_service
    treatment_service_ids = {item.treatment_service_id for item in payload.items}
    for treatment_service_id in treatment_service_ids:
        if crud_treatment_service.get_by_id(db, treatment_service_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Treatment service {treatment_service_id} not found",
            )
    
    seen = set()
    for item in payload.items:
        key = (item.listing_id, item.treatment_service_id)
        if key in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate association: listing {item.listing_id} + treatment_service {item.treatment_service_id}",
            )
        seen.add(key)
    
    from src.models.service import ListingService
    existing_stmt = select(ListingService).where(
        ListingService.listing_id == listing_ids[0],
        ListingService.treatment_service_id.in_(treatment_service_ids),
    )
    existing = db.execute(existing_stmt).scalars().all()
    if existing:
        existing_treatment_service_ids = {e.treatment_service_id for e in existing}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Some treatment services already associated: {existing_treatment_service_ids}",
        )
    
    created = []
    try:
        for item in payload.items:
            obj = crud_listing_service.create(db, item)
            created.append(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create services: {str(e)}",
        )
    
    return created


@router.delete(
    "/listing-services/batch",
    response_model=List[ListingServiceRead],
    dependencies=[Depends(http_bearer)],
    summary="Batch delete listing services",
    description="Delete multiple treatment service associations for a listing in a single request.",
    response_description="List of deleted listing service associations",
)
def batch_delete_listing_services(
    payload: ListingServiceBatchDelete,
    db: DBSession,
    user_id: CurrentUserID,
):
    """Batch delete listing services."""
    listing_ids = [item.listing_id for item in payload.items]
    verify_all_listings_same(db, user_id, listing_ids)
    
    from src.models.service import ListingService
    deleted = []
    
    try:
        for item in payload.items:
            stmt = select(ListingService).where(
                ListingService.listing_id == item.listing_id,
                ListingService.treatment_service_id == item.treatment_service_id,
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj:
                deleted.append(obj)
                db.delete(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete services: {str(e)}",
        )
    
    return deleted

