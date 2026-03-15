from __future__ import annotations

import base64
import uuid
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.storage import delete_image_file, save_image_file
from src.crud.base import CRUDBase
from src.models.listing_image import ListingImage
from src.schemas.listing_image import ListingImageCreate, ListingImageUpdate


class CRUDListingImage(CRUDBase[ListingImage, ListingImageCreate, ListingImageUpdate]):

    def create(self, db: Session, obj_in: ListingImageCreate) -> ListingImage:
        """Create a new listing image, saving file to disk and storing URL in database."""
        # Handle image data: save to disk and store URL
        image_url = obj_in.image_url
        file_size = None
        
        if obj_in.image_data_base64:
            # Decode base64 image data
            image_data_str = obj_in.image_data_base64
            if "," in image_data_str:
                image_data_str = image_data_str.split(",", 1)[1]
            image_data = base64.b64decode(image_data_str)
            
            # Save to disk and get URL
            file_path, url_path = save_image_file(
                image_data,
                filename=obj_in.filename,
                extension=None  # Will be determined from filename
            )
            
            # Store URL instead of binary data
            image_url = url_path
            # Calculate file_size from decoded data
            file_size = len(image_data)
        
        # Create model instance with only the fields that exist in the database
        # Database schema only has: id, listing_id, image_url, display_order, is_primary, created_at
        db_obj = ListingImage(
            listing_id=obj_in.listing_id,
            image_url=image_url,
            display_order=obj_in.display_order,
            is_primary=obj_in.is_primary,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, record_id: uuid.UUID) -> Optional[ListingImage]:
        """Delete an image record and its file from disk."""
        db_obj = self.get_by_id(db, record_id)
        if db_obj is None:
            return None
        
        # Delete file from disk if it's a local file
        if db_obj.image_url and db_obj.image_url.startswith("/uploads/"):
            # Extract relative path from URL
            relative_path = db_obj.image_url.replace("/uploads/", "")
            delete_image_file(relative_path)
        
        db.delete(db_obj)
        db.commit()
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

