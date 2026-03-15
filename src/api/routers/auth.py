from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from src.core.dependencies import CurrentUserID, DBSession
from src.crud.crud_user import crud_user
from src.schemas.user import (
    RefreshTokenRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserRead,
)
from src.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: UserCreate, db: DBSession):
    """Register a new user account. Returns access_token and refresh_token."""
    return auth_service.register_user(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: DBSession):
    """Login with email and password. Returns access_token and refresh_token."""
    return auth_service.login_user(db, payload)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: DBSession):
    """Refresh access token using a valid refresh token."""
    return auth_service.refresh_access_token(db, payload)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshTokenRequest, db: DBSession):
    """Logout by revoking the refresh token."""
    auth_service.logout_user(db, payload.refresh_token)


@router.get("/me", response_model=UserRead)
def get_me(db: DBSession, user_id: CurrentUserID):
    """Return the currently authenticated user's profile."""
    user = crud_user.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

