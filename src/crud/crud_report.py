from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.report import Report
from src.schemas.report import ReportCreate, ReportUpdate


class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):

    def get_pending(self, db: Session, skip: int = 0, limit: int = 20) -> Sequence[Report]:
        stmt = (
            select(Report)
            .where(Report.status == "PENDING")
            .order_by(Report.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()


crud_report = CRUDReport(Report)



