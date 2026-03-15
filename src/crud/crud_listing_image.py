from __future__ import annotations

import base64
import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.listing_image import ListingImage
from src.schemas.listing_image import ListingImageCreate, ListingImageUpdate


class CRUDListingImage(CRUDBase[ListingImage, ListingImageCreate, ListingImageUpdate]):

    def create(self, db: Session, obj_in: ListingImageCreate) -> ListingImage:
        """Create a new listing image, handling base64-encoded image data."""
        data = obj_in.model_dump(exclude={"image_data_base64"})

        # Decode base64 image data if provided
        if obj_in.image_data_base64:
            # Remove data URL prefix if present
            image_data_str = obj_in.image_data_base64
            if "," in image_data_str:
                image_data_str = image_data_str.split(",", 1)[1]
            data["image_data"] = base64.b64decode(image_data_str)
            # Set file_size if not provided
            if "file_size" not in data or data["file_size"] is None:
                data["file_size"] = len(data["image_data"])

        db_obj = ListingImage(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_listing(
        self, db: Session, listing_id: uuid.UUID
    ) -> Sequence[ListingImage]:
        stmt = (
            select(ListingImage)
            .where(ListingImage.listing_id == listing_id)
            .order_by(ListingImage.display_order)
        )
        return db.execute(stmt).scalars().all()


crud_listing_image = CRUDListingImage(ListingImage)

