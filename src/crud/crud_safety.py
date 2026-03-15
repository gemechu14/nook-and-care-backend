from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.safety import ListingSafetyFeature, SafetyFeature
from src.schemas.safety import (
    ListingSafetyFeatureCreate,
    ListingSafetyFeatureRead,
    SafetyFeatureCreate,
    SafetyFeatureUpdate,
)


class CRUDSafetyFeature(CRUDBase[SafetyFeature, SafetyFeatureCreate, SafetyFeatureUpdate]):
    pass


class CRUDListingSafetyFeature(
    CRUDBase[ListingSafetyFeature, ListingSafetyFeatureCreate, ListingSafetyFeatureRead]
):
    pass


crud_safety_feature = CRUDSafetyFeature(SafetyFeature)
crud_listing_safety_feature = CRUDListingSafetyFeature(ListingSafetyFeature)



