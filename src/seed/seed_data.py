"""Seed script to populate initial reference data and a default admin account.

Run with:
    python -m src.seed.seed_data
"""
from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from src.core.logging import get_logger
from src.core.security import hash_password
from src.db.session import SessionLocal

import src.db.base  # noqa: F401 — ensure all models are registered

logger = get_logger(__name__)


# ── Helper ─────────────────────────────────────────────────────────────────────

def _get_or_create(db: Session, model, defaults: dict | None = None, **kwargs):
    """Fetch an existing record or create it."""
    from sqlalchemy import select

    stmt = select(model)
    for key, val in kwargs.items():
        stmt = stmt.where(getattr(model, key) == val)
    obj = db.execute(stmt).scalar_one_or_none()
    if obj is None:
        params = dict(kwargs)
        if defaults:
            params.update(defaults)
        obj = model(**params)
        db.add(obj)
        db.flush()
    return obj, obj is None


# ── Seed functions ─────────────────────────────────────────────────────────────

def seed_admin(db: Session) -> None:
    from src.models.user import User

    admin, created = _get_or_create(
        db,
        User,
        defaults={
            "id": uuid.uuid4(),
            "password_hash": hash_password("Admin@123!"),
            "full_name": "Platform Administrator",
            "role": "ADMIN",
            "is_active": True,
            "email_verified_at": datetime.now(timezone.utc),
        },
        email="admin@nookandcare.com",
    )
    if created:
        logger.info("Admin user created: admin@nookandcare.com")
    else:
        logger.info("Admin user already exists.")


def seed_amenities(db: Session) -> None:
    from src.models.amenity import Amenity

    amenities = [
        {"name": "WiFi", "category": "BASIC"},
        {"name": "Parking", "category": "BASIC"},
        {"name": "Swimming Pool", "category": "PREMIUM"},
        {"name": "Fitness Center", "category": "PREMIUM"},
        {"name": "Garden", "category": "BASIC"},
        {"name": "Library", "category": "BASIC"},
        {"name": "Chapel", "category": "BASIC"},
        {"name": "Beauty Salon", "category": "PREMIUM"},
        {"name": "Emergency Call System", "category": "SAFETY"},
        {"name": "Wheelchair Accessible", "category": "ACCESSIBILITY"},
        {"name": "Air Conditioning", "category": "BASIC"},
        {"name": "Laundry Services", "category": "BASIC"},
        {"name": "Private Dining", "category": "PREMIUM"},
        {"name": "Transportation Services", "category": "BASIC"},
        {"name": "24-Hour Security", "category": "SAFETY"},
    ]
    for item in amenities:
        _get_or_create(db, Amenity, defaults={"id": uuid.uuid4()}, name=item["name"], category=item["category"])
    logger.info(f"Seeded {len(amenities)} amenities.")


def seed_activities(db: Session) -> None:
    from src.models.activity import Activity

    activities = [
        {"name": "Gardening Club", "category": "RECREATIONAL"},
        {"name": "Game Nights", "category": "SOCIAL"},
        {"name": "Art Classes", "category": "RECREATIONAL"},
        {"name": "Yoga", "category": "FITNESS"},
        {"name": "Movie Nights", "category": "SOCIAL"},
        {"name": "Music Therapy", "category": "RECREATIONAL"},
        {"name": "Book Club", "category": "EDUCATIONAL"},
        {"name": "Walking Groups", "category": "FITNESS"},
        {"name": "Cooking Classes", "category": "EDUCATIONAL"},
        {"name": "Bingo", "category": "SOCIAL"},
    ]
    for item in activities:
        _get_or_create(db, Activity, defaults={"id": uuid.uuid4()}, name=item["name"], category=item["category"])
    logger.info(f"Seeded {len(activities)} activities.")


def seed_languages(db: Session) -> None:
    from src.models.language import Language

    languages = [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "zh", "name": "Chinese"},
        {"code": "tl", "name": "Tagalog"},
        {"code": "ko", "name": "Korean"},
        {"code": "vi", "name": "Vietnamese"},
        {"code": "ar", "name": "Arabic"},
    ]
    for item in languages:
        _get_or_create(db, Language, defaults={"id": uuid.uuid4(), "name": item["name"]}, code=item["code"])
    logger.info(f"Seeded {len(languages)} languages.")


def seed_certifications(db: Session) -> None:
    from src.models.certification import Certification

    certs = [
        {"name": "State Licensed", "description": "Licensed by the state health department"},
        {"name": "Medicare Certified", "description": "Certified to accept Medicare"},
        {"name": "Medicaid Certified", "description": "Certified to accept Medicaid"},
        {"name": "VA Approved", "description": "Approved by the Department of Veterans Affairs"},
        {"name": "Joint Commission Accredited", "description": "Accredited by The Joint Commission"},
    ]
    for item in certs:
        _get_or_create(db, Certification, defaults={"id": uuid.uuid4(), "description": item["description"]}, name=item["name"])
    logger.info(f"Seeded {len(certs)} certifications.")


def seed_dining_options(db: Session) -> None:
    from src.models.dining import DiningOption

    options = [
        {"name": "Three home-cooked meals daily"},
        {"name": "Special dietary accommodations"},
        {"name": "Family-style dining"},
        {"name": "Restaurant-style dining"},
        {"name": "In-room dining available"},
        {"name": "Vegetarian options"},
        {"name": "Kosher meals"},
        {"name": "Halal meals"},
    ]
    for item in options:
        _get_or_create(db, DiningOption, defaults={"id": uuid.uuid4()}, name=item["name"])
    logger.info(f"Seeded {len(options)} dining options.")


def seed_safety_features(db: Session) -> None:
    from src.models.safety import SafetyFeature

    features = [
        {"name": "Emergency Call System", "category": "EMERGENCY"},
        {"name": "Fire Suppression System", "category": "FIRE"},
        {"name": "Smoke Detectors", "category": "FIRE"},
        {"name": "Fall Prevention Program", "category": "MEDICAL"},
        {"name": "Wheelchair Ramps", "category": "ACCESSIBILITY"},
        {"name": "Grab Bars", "category": "ACCESSIBILITY"},
        {"name": "Secured Entry", "category": "EMERGENCY"},
        {"name": "Memory Care Security", "category": "EMERGENCY"},
    ]
    for item in features:
        _get_or_create(db, SafetyFeature, defaults={"id": uuid.uuid4(), "category": item["category"]}, name=item["name"])
    logger.info(f"Seeded {len(features)} safety features.")


def seed_insurance_options(db: Session) -> None:
    from src.models.insurance import InsuranceOption

    options = [
        {"name": "Medicare"},
        {"name": "Medicaid"},
        {"name": "Private Insurance"},
        {"name": "Long-term Care Insurance"},
        {"name": "VA Benefits"},
        {"name": "Private Pay"},
    ]
    for item in options:
        _get_or_create(db, InsuranceOption, defaults={"id": uuid.uuid4()}, name=item["name"])
    logger.info(f"Seeded {len(options)} insurance options.")


def seed_house_rules(db: Session) -> None:
    from src.models.house_rule import HouseRule

    rules = [
        {"name": "No Smoking", "category": "SMOKING"},
        {"name": "No Pets", "category": "PET"},
        {"name": "Pets Allowed", "category": "PET"},
        {"name": "Quiet Hours 10pm–7am", "category": "QUIET_HOURS"},
        {"name": "Visitor Sign-in Required", "category": "VISITOR"},
        {"name": "No Overnight Guests", "category": "VISITOR"},
    ]
    for item in rules:
        _get_or_create(db, HouseRule, defaults={"id": uuid.uuid4(), "category": item["category"]}, name=item["name"])
    logger.info(f"Seeded {len(rules)} house rules.")


def seed_treatment_services(db: Session) -> None:
    from src.models.service import TreatmentService

    services = [
        {"name": "Medication Management"},
        {"name": "Diabetes Management"},
        {"name": "Physical Therapy"},
        {"name": "Occupational Therapy"},
        {"name": "Speech Therapy"},
        {"name": "Wound Care"},
        {"name": "Incontinence Care"},
        {"name": "Dementia Care"},
        {"name": "Hospice Care"},
        {"name": "Respite Care"},
    ]
    for item in services:
        _get_or_create(db, TreatmentService, defaults={"id": uuid.uuid4()}, name=item["name"])
    logger.info(f"Seeded {len(services)} treatment services.")


def seed_equipment(db: Session) -> None:
    from src.models.equipment import Equipment

    equipment_items = [
        {"name": "Hospital Bed", "category": "MEDICAL", "description": "Adjustable bed for patient comfort and care"},
        {"name": "Wheelchair", "category": "MOBILITY", "description": "Manual wheelchair for resident mobility"},
        {"name": "Walker", "category": "MOBILITY", "description": "Standard walker for assisted walking"},
        {"name": "Shower Chair", "category": "SAFETY", "description": "Water-resistant chair for safe bathing"},
        {"name": "Grab Bars", "category": "SAFETY", "description": "Mounted bars in bathrooms and hallways"},
        {"name": "Oxygen Concentrator", "category": "MEDICAL", "description": "Device for supplemental oxygen therapy"},
        {"name": "Blood Pressure Monitor", "category": "MEDICAL", "description": "Digital monitor for blood pressure checks"},
        {"name": "Pulse Oximeter", "category": "MEDICAL", "description": "Device to measure oxygen saturation levels"},
        {"name": "Patient Lift", "category": "MOBILITY", "description": "Mechanical lift for safe resident transfers"},
        {"name": "Nebulizer", "category": "MEDICAL", "description": "Respiratory treatment device"},
        {"name": "Recliner Chair", "category": "COMFORT", "description": "Supportive recliner for elderly residents"},
        {"name": "Bedside Commode", "category": "SAFETY", "description": "Portable toilet for residents with limited mobility"},
        {"name": "Hearing Assistance Device", "category": "ASSISTIVE", "description": "Amplification device for hearing support"},
        {"name": "Medication Cart", "category": "CARE", "description": "Secure cart for medication storage and rounds"},
        {"name": "Emergency Call Button", "category": "SAFETY", "description": "Resident alert system for emergency assistance"},
    ]

    for item in equipment_items:
        _get_or_create(
            db,
            Equipment,
            defaults={"id": uuid.uuid4(), "description": item["description"]},
            name=item["name"],
            category=item["category"],
        )

    logger.info(f"Seeded {len(equipment_items)} equipment items.")


def seed_sample_provider_and_listing(db: Session) -> None:
    """Create a sample verified provider with one active listing."""
    from src.models.user import User
    from src.models.provider import Provider
    from src.models.listing import Listing
    from src.models.listing_image import ListingImage

    # Provider user
    provider_user, user_created = _get_or_create(
        db,
        User,
        defaults={
            "id": uuid.uuid4(),
            "password_hash": hash_password("Provider@123!"),
            "full_name": "Sunrise Gardens Staff",
            "role": "PROVIDER",
            "is_active": True,
            "email_verified_at": datetime.now(timezone.utc),
        },
        email="provider@sunrisegardens.com",
    )

    # Provider profile
    provider, prov_created = _get_or_create(
        db,
        Provider,
        defaults={
            "id": uuid.uuid4(),
            "business_name": "Sunrise Gardens Senior Living",
            "business_type": "ASSISTED_LIVING",
            "address": "123 Sunrise Blvd",
            "city": "Los Angeles",
            "country": "USA",
            "verification_status": "VERIFIED",
            "verified_at": datetime.now(timezone.utc),
        },
        user_id=provider_user.id,
    )

    # Listing
    listing, listing_created = _get_or_create(
        db,
        Listing,
        defaults={
            "id": uuid.uuid4(),
            "title": "Sunrise Gardens Assisted Living",
            "description": (
                "A warm, welcoming assisted living community in the heart of Los Angeles. "
                "We provide 24-hour personalized care with a focus on comfort and dignity."
            ),
            "care_type": "ASSISTED_LIVING",
            "room_type": "PRIVATE",
            "address": "123 Sunrise Blvd",
            "city": "Los Angeles",
            "state": "CA",
            "country": "USA",
            "postal_code": "90001",
            "latitude": 34.052235,
            "longitude": -118.243683,
            "price": 4500.00,
            "currency": "USD",
            "capacity": 50,
            "available_beds": 8,
            "staff_ratio": "1:4",
            "established_year": 2005,
            "phone": "+1-213-555-0100",
            "email": "info@sunrisegardens.com",
            "has_24_hour_care": True,
            "is_featured": True,
            "status": "ACTIVE",
        },
        provider_id=provider.id,
        title="Sunrise Gardens Assisted Living",
    )

    if listing_created:
        # Add a placeholder image (using URL for seed data - can be replaced with binary later)
        img = ListingImage(
            id=uuid.uuid4(),
            listing_id=listing.id,
            image_url="https://images.unsplash.com/photo-1586105251261-72a756497a11?w=800",
            filename="placeholder.jpg",
            content_type="image/jpeg",
            display_order=0,
            is_primary=True,
        )
        db.add(img)
        logger.info("Sample listing created: Sunrise Gardens Assisted Living")
    else:
        logger.info("Sample listing already exists.")


def run_seed() -> None:
    db: Session = SessionLocal()
    try:
        logger.info("Starting seed …")
        seed_admin(db)
        seed_amenities(db)
        seed_activities(db)
        seed_languages(db)
        seed_certifications(db)
        seed_dining_options(db)
        seed_safety_features(db)
        seed_insurance_options(db)
        seed_house_rules(db)
        seed_treatment_services(db)
        seed_equipment(db)
        seed_sample_provider_and_listing(db)
        db.commit()
        logger.info("Seed completed successfully.")
    except Exception as exc:
        db.rollback()
        logger.error(f"Seed failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Ensure tables exist before seeding
    from src.db.init_db import init_db
    init_db()
    run_seed()

