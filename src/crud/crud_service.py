from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.service import ListingService, TreatmentService
from src.schemas.service import (
    ListingServiceCreate,
    ListingServiceUpdate,
    TreatmentServiceCreate,
    TreatmentServiceUpdate,
)


class CRUDTreatmentService(
    CRUDBase[TreatmentService, TreatmentServiceCreate, TreatmentServiceUpdate]
):
    pass


class CRUDListingService(CRUDBase[ListingService, ListingServiceCreate, ListingServiceUpdate]):
    pass


crud_treatment_service = CRUDTreatmentService(TreatmentService)
crud_listing_service = CRUDListingService(ListingService)






