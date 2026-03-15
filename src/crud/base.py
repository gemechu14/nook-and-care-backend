from __future__ import annotations

from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generic CRUD base class.

    Provides default create / get_by_id / get_all / update / delete operations.
    Override any method in a subclass for custom behavior.
    """

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_by_id(self, db: Session, record_id: Any) -> Optional[ModelType]:
        """Return a single record by primary key, or None if not found."""
        stmt = select(self.model).where(self.model.id == record_id)
        return db.execute(stmt).scalar_one_or_none()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[ModelType]:
        """Return a paginated list of records."""
        stmt = select(self.model).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    # ── Write ─────────────────────────────────────────────────────────────────

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record from a Pydantic schema."""
        data = obj_in.model_dump()
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        """Update an existing record from a Pydantic schema (partial update)."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, record_id: Any) -> Optional[ModelType]:
        """Delete a record by primary key. Returns deleted object or None."""
        db_obj = self.get_by_id(db, record_id)
        if db_obj is None:
            return None
        db.delete(db_obj)
        db.commit()
        return db_obj





