from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.security import create_access_token, create_refresh_token
from src.crud.crud_refresh_token import crud_refresh_token
from src.crud.crud_user import crud_user
from src.models.refresh_token import RefreshToken
from src.schemas.user import RefreshTokenRequest, TokenResponse, UserCreate, UserLogin


def register_user(db: Session, payload: UserCreate) -> TokenResponse:
    """Register a new user and return access + refresh tokens."""
    if crud_user.get_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = crud_user.create(db, payload)

    # Generate tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token_str, expires_at = create_refresh_token(str(user.id))

    # Store refresh token in database
    refresh_token = RefreshToken(
        user_id=user.id, token=refresh_token_str, expires_at=expires_at
    )
    db.add(refresh_token)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token_str)


def login_user(db: Session, payload: UserLogin) -> TokenResponse:
    """Authenticate a user and return access + refresh tokens."""
    user = crud_user.authenticate(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is deactivated",
        )

    # Generate tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token_str, expires_at = create_refresh_token(str(user.id))

    # Store refresh token in database
    refresh_token = RefreshToken(
        user_id=user.id, token=refresh_token_str, expires_at=expires_at
    )
    db.add(refresh_token)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token_str)


def refresh_access_token(db: Session, payload: RefreshTokenRequest) -> TokenResponse:
    """Generate a new access token using a valid refresh token."""
    # Validate refresh token
    if not crud_refresh_token.is_valid(db, payload.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get the refresh token record
    refresh_token = crud_refresh_token.get_by_token(db, payload.refresh_token)
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )

    # Generate new access token
    access_token = create_access_token(subject=str(refresh_token.user_id))

    # Return new access token (refresh token remains valid until expiry)
    return TokenResponse(
        access_token=access_token, refresh_token=payload.refresh_token
    )


def logout_user(db: Session, refresh_token: str) -> None:
    """Revoke a refresh token (logout)."""
    revoked = crud_refresh_token.revoke_token(db, refresh_token)
    if revoked is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Refresh token not found"
        )

