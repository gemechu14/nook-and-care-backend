from __future__ import annotations

from fastapi import APIRouter

from src.api.routers.auth import router as auth_router
from src.api.routers.users import router as users_router
from src.api.routers.providers import router as providers_router
from src.api.routers.dashboard import router as dashboard_router
from src.api.routers.listings import router as listings_router
from src.api.routers.listing_images import router as listing_images_router
from src.api.routers.tours import router as tours_router
from src.api.routers.reviews import router as reviews_router
from src.api.routers.favorites import router as favorites_router
from src.api.routers.subscriptions import router as subscriptions_router
from src.api.routers.payments import router as payments_router
from src.api.routers.reports import router as reports_router
from src.api.routers.listing_features import router as listing_features_router
from src.api.routers.catalog import (
    amenities_router,
    activities_router,
    languages_router,
    certifications_router,
    dining_router,
    safety_router,
    insurance_router,
    house_rules_router,
    equipment_router,
    services_router,
)

api_router = APIRouter(prefix="/api/v1")

# ── Core domain routers ───────────────────────────────────────────────────────
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(providers_router)
api_router.include_router(dashboard_router)
api_router.include_router(listings_router)
api_router.include_router(listing_images_router)
api_router.include_router(tours_router)
api_router.include_router(reviews_router)
api_router.include_router(favorites_router)
api_router.include_router(subscriptions_router)
api_router.include_router(payments_router)
api_router.include_router(reports_router)
api_router.include_router(listing_features_router)

# ── Catalog / lookup routers ──────────────────────────────────────────────────
api_router.include_router(amenities_router)
api_router.include_router(activities_router)
api_router.include_router(languages_router)
api_router.include_router(certifications_router)
api_router.include_router(dining_router)
api_router.include_router(safety_router)
api_router.include_router(insurance_router)
api_router.include_router(house_rules_router)
api_router.include_router(equipment_router)
api_router.include_router(services_router)

