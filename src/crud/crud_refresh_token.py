from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.refresh_token import RefreshToken
from src.schemas.refresh_token import RefreshTokenCreate, RefreshTokenRead


class CRUDRefreshToken(CRUDBase[RefreshToken, RefreshTokenCreate, RefreshTokenRead]):

    def get_by_token(self, db: Session, token: str) -> Optional[RefreshToken]:
        """Find a refresh token by its token string (including revoked ones)."""
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        return db.execute(stmt).scalar_one_or_none()

    def is_valid(self, db: Session, token: str) -> bool:
        """Check if a refresh token is valid (exists, not revoked, not expired)."""
        refresh_token = self.get_by_token(db, token)
        if refresh_token is None:
            return False
        if refresh_token.is_revoked:
            return False
        if refresh_token.expires_at < datetime.now(timezone.utc):
            return False
        return True

    def revoke_token(self, db: Session, token: str) -> Optional[RefreshToken]:
        """Revoke a refresh token."""
        refresh_token = self.get_by_token(db, token)
        if refresh_token is None:
            return None
        refresh_token.is_revoked = True
        db.commit()
        db.refresh(refresh_token)
        return refresh_token

    def revoke_all_user_tokens(self, db: Session, user_id: uuid.UUID) -> int:
        """Revoke all refresh tokens for a user (e.g., on password change)."""
        from sqlalchemy import update

        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
            )
            .values(is_revoked=True)
        )
        result = db.execute(stmt)
        db.commit()
        return result.rowcount


crud_refresh_token = CRUDRefreshToken(RefreshToken)

