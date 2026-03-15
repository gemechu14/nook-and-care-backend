from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.core.security import decode_access_token
from src.db.session import get_db

# Use HTTPBearer for simpler Bearer token authentication in Swagger UI
http_bearer = HTTPBearer(auto_error=False)

# ── Typed aliases ──────────────────────────────────────────────────────────────

DBSession = Annotated[Session, Depends(get_db)]


# ── Current user dependency ───────────────────────────────────────────────────

def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)]
) -> str:
    """Decode JWT and return the subject (user id) string.

    Raises 401 if token is missing, invalid, or expired.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
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

def pagination_params(
    page: Annotated[int, Query(ge=1, description="Page number (1-indexed)", example=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100, description="Number of items per page (max 100)", example=20)] = 20,
) -> tuple[int, int]:
    """Common page/size pagination parameters.
    
    Converts page/size to skip/limit for database queries.
    - page: Page number (1-indexed, default: 1)
    - size: Number of items per page (max 100, default: 20)
    Returns: (skip, limit) tuple
    """
    if page < 1:
        page = 1
    size = min(size, 100)  # cap to MAX_PAGE_SIZE
    skip = (page - 1) * size
    return skip, size


PaginationParams = Annotated[
    tuple[int, int],
    Depends(pagination_params),
]


