"""Run only the equipment seed.

From project root:
    python -m src.seed.equipment

Or from anywhere (e.g. src/seed):
    python equipment.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Add project root so "src" can be imported when run as python equipment.py
_project_root = Path(__file__).resolve().parent.parent.parent
if _project_root not in sys.path:
    sys.path.insert(0, str(_project_root))
# Ensure .env is resolved from project root and relative DB paths are correct.
os.chdir(_project_root)

from src.db.init_db import init_db
from src.db.session import SessionLocal
from src.seed.seed_data import seed_equipment

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        seed_equipment(db)
        db.commit()
        print("Equipment seed completed.")
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
