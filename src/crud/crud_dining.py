from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.dining import DiningOption, ListingDiningOption
from src.schemas.dining import (
    DiningOptionCreate,
    DiningOptionUpdate,
    ListingDiningOptionCreate,
    ListingDiningOptionRead,
)


class CRUDDiningOption(CRUDBase[DiningOption, DiningOptionCreate, DiningOptionUpdate]):
    pass


class CRUDListingDiningOption(
    CRUDBase[ListingDiningOption, ListingDiningOptionCreate, ListingDiningOptionRead]
):
    pass


crud_dining_option = CRUDDiningOption(DiningOption)
crud_listing_dining_option = CRUDListingDiningOption(ListingDiningOption)







