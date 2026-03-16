from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.certification import Certification, ListingCertification
from src.schemas.certification import (
    CertificationCreate,
    CertificationUpdate,
    ListingCertificationCreate,
    ListingCertificationUpdate,
)


class CRUDCertification(CRUDBase[Certification, CertificationCreate, CertificationUpdate]):
    pass


class CRUDListingCertification(
    CRUDBase[ListingCertification, ListingCertificationCreate, ListingCertificationUpdate]
):
    pass


crud_certification = CRUDCertification(Certification)
crud_listing_certification = CRUDListingCertification(ListingCertification)







