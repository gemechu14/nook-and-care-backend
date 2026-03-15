from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.api.api_v1 import api_router
from src.core.config import settings
from src.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown hooks."""
    configure_logging()

    # In development, auto-create tables so the app works without running
    # Alembic migrations manually.
    if settings.is_development:
        from src.db.init_db import init_db
        init_db()

    yield
    # Shutdown: nothing to clean up yet


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "**Nook and Care** — Senior Housing Marketplace API\n\n"
        "Manage listings, tours, reviews, subscriptions, and more."
    ),
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


def custom_openapi():
    """Custom OpenAPI schema with Bearer token authentication."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "**Nook and Care** — Senior Housing Marketplace API\n\n"
            "Manage listings, tours, reviews, subscriptions, and more.\n\n"
            "## Authentication\n\n"
            "Most endpoints require authentication. Use the **Authorize** button above to paste your Bearer token.\n\n"
            "1. Login via `/api/v1/auth/login` to get an `access_token`\n"
            "2. Click the **Authorize** button (lock icon) in Swagger UI\n"
            "3. Paste your token (without 'Bearer' prefix)\n"
            "4. Click **Authorize** and **Close**\n"
            "5. All authenticated requests will now include the token"
        ),
        routes=app.routes,
    )
    
    # Ensure components exist
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}
    
    # HTTPBearer automatically adds "HTTPBearer" scheme, enhance it with description
    openapi_schema["components"]["securitySchemes"]["HTTPBearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Enter your JWT access token. Get it from `/api/v1/auth/login` endpoint. Just paste the token (no 'Bearer' prefix needed).",
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Override OpenAPI schema to add Bearer token authentication
app.openapi = custom_openapi

# ── CORS ──────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(api_router)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok", "version": settings.APP_VERSION}


