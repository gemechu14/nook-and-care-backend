from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.insurance import InsuranceOption, ListingInsuranceOption
from src.schemas.insurance import (
    InsuranceOptionCreate,
    InsuranceOptionUpdate,
    ListingInsuranceOptionCreate,
    ListingInsuranceOptionRead,
)


class CRUDInsuranceOption(
    CRUDBase[InsuranceOption, InsuranceOptionCreate, InsuranceOptionUpdate]
):
    pass


class CRUDListingInsuranceOption(
    CRUDBase[ListingInsuranceOption, ListingInsuranceOptionCreate, ListingInsuranceOptionRead]
):
    pass


crud_insurance_option = CRUDInsuranceOption(InsuranceOption)
crud_listing_insurance_option = CRUDListingInsuranceOption(ListingInsuranceOption)






