from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.amenity import AmenityRead
from src.schemas.language import LanguageRead
from src.schemas.certification import CertificationRead
from src.schemas.activity import ActivityRead
from src.schemas.dining import DiningOptionRead
from src.schemas.safety import SafetyFeatureRead
from src.schemas.insurance import InsuranceOptionRead
from src.schemas.house_rule import HouseRuleRead
from src.schemas.equipment import EquipmentRead
from src.schemas.service import TreatmentServiceRead, ListingServiceRead
from src.schemas.listing_image import ListingImageRead


class ListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    care_type: str  # ASSISTED_LIVING | MEMORY_CARE | INDEPENDENT_LIVING | ADULT_FAMILY_HOME | SKILLED_NURSING
    room_type: str  # PRIVATE | SEMI_PRIVATE | SHARED
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price: Optional[float] = None
    currency: str = "USD"
    capacity: Optional[int] = None
    available_beds: Optional[int] = None
    staff_ratio: Optional[str] = None
    established_year: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    license_number: Optional[str] = None
    is_featured: bool = False
    has_24_hour_care: bool = False


class ListingCreate(ListingBase):
    provider_id: uuid.UUID


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    care_type: Optional[str] = None
    room_type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    capacity: Optional[int] = None
    available_beds: Optional[int] = None
    staff_ratio: Optional[str] = None
    established_year: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    license_number: Optional[str] = None
    is_featured: Optional[bool] = None
    has_24_hour_care: Optional[bool] = None
    status: Optional[str] = None


# ── Nested schemas for listing relationships ──────────────────────────────────

class ListingAmenityWithDetails(BaseModel):
    """Amenity with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    amenity: AmenityRead
    created_at: datetime


class ListingLanguageWithDetails(BaseModel):
    """Language with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    language: LanguageRead
    created_at: datetime


class ListingCertificationWithDetails(BaseModel):
    """Certification with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    certification: CertificationRead
    license_number: Optional[str] = None
    created_at: datetime


class ListingActivityWithDetails(BaseModel):
    """Activity with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    activity: ActivityRead
    created_at: datetime


class ListingDiningOptionWithDetails(BaseModel):
    """Dining option with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    dining_option: DiningOptionRead
    created_at: datetime


class ListingSafetyFeatureWithDetails(BaseModel):
    """Safety feature with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    safety_feature: SafetyFeatureRead
    created_at: datetime


class ListingInsuranceOptionWithDetails(BaseModel):
    """Insurance option with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    insurance_option: InsuranceOptionRead
    created_at: datetime


class ListingHouseRuleWithDetails(BaseModel):
    """House rule with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    house_rule: HouseRuleRead
    display_order: int
    created_at: datetime


class ListingEquipmentWithDetails(BaseModel):
    """Equipment with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    equipment: EquipmentRead
    quantity: int
    created_at: datetime


class ListingServiceWithDetails(BaseModel):
    """Treatment service with full details for listing response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    treatment_service: TreatmentServiceRead
    price: Optional[float] = None
    is_included: bool
    created_at: datetime


class ListingListRead(ListingBase):
    """Simplified listing schema for list endpoints without nested relationships."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    provider_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime


class ListingRead(ListingBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    provider_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    
    # Related data - using model attribute names with aliases for cleaner JSON output
    images: List[ListingImageRead] = Field(default_factory=list)
    listing_amenities: List[ListingAmenityWithDetails] = Field(default_factory=list, alias="amenities")
    listing_languages: List[ListingLanguageWithDetails] = Field(default_factory=list, alias="languages")
    listing_certifications: List[ListingCertificationWithDetails] = Field(default_factory=list, alias="certifications")
    listing_activities: List[ListingActivityWithDetails] = Field(default_factory=list, alias="activities")
    listing_dining_options: List[ListingDiningOptionWithDetails] = Field(default_factory=list, alias="dining_options")
    listing_safety_features: List[ListingSafetyFeatureWithDetails] = Field(default_factory=list, alias="safety_features")
    listing_insurance_options: List[ListingInsuranceOptionWithDetails] = Field(default_factory=list, alias="insurance_options")
    listing_house_rules: List[ListingHouseRuleWithDetails] = Field(default_factory=list, alias="house_rules")
    listing_equipment: List[ListingEquipmentWithDetails] = Field(default_factory=list, alias="equipment")
    listing_services: List[ListingServiceWithDetails] = Field(default_factory=list, alias="services")





