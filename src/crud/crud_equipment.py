from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.equipment import Equipment, ListingEquipment
from src.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    ListingEquipmentCreate,
    ListingEquipmentUpdate,
)


class CRUDEquipment(CRUDBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    pass


class CRUDListingEquipment(
    CRUDBase[ListingEquipment, ListingEquipmentCreate, ListingEquipmentUpdate]
):
    pass


crud_equipment = CRUDEquipment(Equipment)
crud_listing_equipment = CRUDListingEquipment(ListingEquipment)


