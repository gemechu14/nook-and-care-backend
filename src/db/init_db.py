from __future__ import annotations

from sqlalchemy import inspect

from src.core.logging import get_logger
from src.db.session import Base, engine

logger = get_logger(__name__)


def init_db() -> None:
    """Create all tables based on registered models.

    This is used for **development / testing only**.
    In production, always use Alembic migrations.

    Only creates tables if they don't already exist.
    """
    # Import all models so they are registered with Base.metadata
    import src.db.base  # noqa: F401

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    # Check if any of our tables are missing
    required_tables = set(Base.metadata.tables.keys())
    missing_tables = required_tables - existing_tables

    if missing_tables:
        logger.info(f"Creating {len(missing_tables)} missing database tables …")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created.")
    else:
        logger.debug("All database tables already exist. Skipping table creation.")

