from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.crud.crud_report import crud_report
from src.models.report import Report
from src.schemas.report import ReportCreate


def file_report(db: Session, payload: ReportCreate) -> Report:
    """File a new report (by a user against a listing or provider)."""
    return crud_report.create(db, payload)


def review_report(db: Session, report_id: uuid.UUID) -> Report:
    """Mark a report as REVIEWED (admin action)."""
    report = crud_report.get_by_id(db, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    report.status = "REVIEWED"
    db.commit()
    db.refresh(report)
    return report


def resolve_report(db: Session, report_id: uuid.UUID) -> Report:
    """Mark a report as RESOLVED (admin action)."""
    report = crud_report.get_by_id(db, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    report.status = "RESOLVED"
    db.commit()
    db.refresh(report)
    return report


def dismiss_report(db: Session, report_id: uuid.UUID) -> Report:
    """Mark a report as DISMISSED (admin action)."""
    report = crud_report.get_by_id(db, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    report.status = "DISMISSED"
    db.commit()
    db.refresh(report)
    return report





