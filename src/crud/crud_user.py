from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.security import hash_password
from src.crud.base import CRUDBase
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Look up a user by email address."""
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        """Create a new user with a hashed password."""
        data = obj_in.model_dump(exclude={"password"})
        data["password_hash"] = hash_password(obj_in.password)
        db_obj = User(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        """Return user if credentials are valid, else None."""
        from src.core.security import verify_password

        user = self.get_by_email(db, email)
        if user is None:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user


crud_user = CRUDUser(User)

# Convenience aliases used in dependencies.py
get_by_id = crud_user.get_by_id


