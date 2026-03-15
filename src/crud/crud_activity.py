from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.activity import Activity, ListingActivity
from src.schemas.activity import (
    ActivityCreate,
    ActivityUpdate,
    ListingActivityCreate,
    ListingActivityRead,
)


class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    pass


class CRUDListingActivity(CRUDBase[ListingActivity, ListingActivityCreate, ListingActivityRead]):
    pass


crud_activity = CRUDActivity(Activity)
crud_listing_activity = CRUDListingActivity(ListingActivity)





