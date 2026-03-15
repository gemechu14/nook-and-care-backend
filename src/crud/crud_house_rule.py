from __future__ import annotations

from src.crud.base import CRUDBase
from src.models.house_rule import HouseRule, ListingHouseRule
from src.schemas.house_rule import (
    HouseRuleCreate,
    HouseRuleUpdate,
    ListingHouseRuleCreate,
    ListingHouseRuleUpdate,
)


class CRUDHouseRule(CRUDBase[HouseRule, HouseRuleCreate, HouseRuleUpdate]):
    pass


class CRUDListingHouseRule(
    CRUDBase[ListingHouseRule, ListingHouseRuleCreate, ListingHouseRuleUpdate]
):
    pass


crud_house_rule = CRUDHouseRule(HouseRule)
crud_listing_house_rule = CRUDListingHouseRule(ListingHouseRule)



