# This module imports every SQLAlchemy model so that Alembic's autogenerate
# command can discover all table definitions from Base.metadata.
#
# Import order matters: models with no FK deps first, then dependent models.

from src.db.session import Base  # noqa: F401 — re-export Base

# ── Core user / provider models ───────────────────────────────────────────────
from src.models.user import User  # noqa: F401
from src.models.provider import Provider  # noqa: F401
from src.models.refresh_token import RefreshToken  # noqa: F401

# ── Catalog / lookup tables ────────────────────────────────────────────────────
from src.models.amenity import Amenity  # noqa: F401
from src.models.service import TreatmentService  # noqa: F401
from src.models.equipment import Equipment  # noqa: F401
from src.models.language import Language  # noqa: F401
from src.models.certification import Certification  # noqa: F401
from src.models.activity import Activity  # noqa: F401
from src.models.dining import DiningOption  # noqa: F401
from src.models.safety import SafetyFeature  # noqa: F401
from src.models.insurance import InsuranceOption  # noqa: F401
from src.models.house_rule import HouseRule  # noqa: F401

# ── Listing and its junction tables ───────────────────────────────────────────
from src.models.listing import Listing  # noqa: F401
from src.models.listing_image import ListingImage  # noqa: F401
from src.models.amenity import ListingAmenity  # noqa: F401
from src.models.service import ListingService  # noqa: F401
from src.models.equipment import ListingEquipment  # noqa: F401
from src.models.language import ListingLanguage  # noqa: F401
from src.models.certification import ListingCertification  # noqa: F401
from src.models.activity import ListingActivity  # noqa: F401
from src.models.dining import ListingDiningOption  # noqa: F401
from src.models.safety import ListingSafetyFeature  # noqa: F401
from src.models.insurance import ListingInsuranceOption  # noqa: F401
from src.models.house_rule import ListingHouseRule  # noqa: F401

# ── Transactional models ───────────────────────────────────────────────────────
from src.models.tour import Tour  # noqa: F401
from src.models.review import Review  # noqa: F401
from src.models.favorite import Favorite  # noqa: F401
from src.models.subscription import Subscription  # noqa: F401
from src.models.payment import Payment  # noqa: F401
from src.models.report import Report  # noqa: F401

