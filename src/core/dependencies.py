from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.core.security import decode_access_token
from src.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ── Typed aliases ──────────────────────────────────────────────────────────────

DBSession = Annotated[Session, Depends(get_db)]


# ── Current user dependency ───────────────────────────────────────────────────

def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """Decode JWT and return the subject (user id) string.

    Raises 401 if token is missing, invalid, or expired.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


CurrentUserID = Annotated[str, Depends(get_current_user_id)]


def require_role(*roles: str):
    """Dependency factory that checks the current user has one of the given roles.

    Usage::

        @router.get("/admin")
        def admin_only(
            db: DBSession,
            user_id: CurrentUserID,
            _: None = Depends(require_role("ADMIN")),
        ):
            ...
    """

    def _check(db: DBSession, user_id: CurrentUserID) -> None:
        from src.crud.crud_user import get_by_id as get_user

        user = get_user(db, user_id)
        if user is None or user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

    return _check


# ── Pagination helpers ────────────────────────────────────────────────────────

def pagination_params(skip: int = 0, limit: int = 20) -> tuple[int, int]:
    """Common skip/limit pagination parameters."""
    limit = min(limit, 100)  # cap to MAX_PAGE_SIZE
    return skip, limit


PaginationParams = Annotated[tuple[int, int], Depends(pagination_params)]


