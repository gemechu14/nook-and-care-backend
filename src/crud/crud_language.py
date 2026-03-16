from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.language import Language, ListingLanguage
from src.schemas.language import (
    LanguageCreate,
    LanguageUpdate,
    ListingLanguageCreate,
    ListingLanguageRead,
)


class CRUDLanguage(CRUDBase[Language, LanguageCreate, LanguageUpdate]):
    pass


class CRUDListingLanguage(CRUDBase[ListingLanguage, ListingLanguageCreate, ListingLanguageRead]):
    pass


crud_language = CRUDLanguage(Language)
crud_listing_language = CRUDListingLanguage(ListingLanguage)






