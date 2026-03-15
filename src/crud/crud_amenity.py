from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.amenity import Amenity, ListingAmenity
from src.schemas.amenity import AmenityCreate, AmenityUpdate, ListingAmenityCreate


class CRUDAmenity(CRUDBase[Amenity, AmenityCreate, AmenityUpdate]):
    pass


class CRUDListingAmenity(CRUDBase[ListingAmenity, ListingAmenityCreate, ListingAmenityCreate]):
    pass


crud_amenity = CRUDAmenity(Amenity)
crud_listing_amenity = CRUDListingAmenity(ListingAmenity)





