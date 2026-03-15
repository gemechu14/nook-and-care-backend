from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import DBSession, PaginationParams, http_bearer
from src.crud.crud_report import crud_report
from src.schemas.report import ReportCreate, ReportRead, ReportUpdate
from src.services import report_service

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(http_bearer)],
)


@router.get("/", response_model=List[ReportRead])
def list_reports(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_report.get_all(db, skip=skip, limit=limit)


@router.get("/{report_id}", response_model=ReportRead)
def get_report(report_id: uuid.UUID, db: DBSession):
    report = crud_report.get_by_id(db, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.post("/", response_model=ReportRead, status_code=201)
def file_report(payload: ReportCreate, db: DBSession):
    return report_service.file_report(db, payload)


@router.put("/{report_id}", response_model=ReportRead)
def update_report(report_id: uuid.UUID, payload: ReportUpdate, db: DBSession):
    report = crud_report.get_by_id(db, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return crud_report.update(db, report, payload)


@router.post("/{report_id}/review", response_model=ReportRead)
def review_report(report_id: uuid.UUID, db: DBSession):
    return report_service.review_report(db, report_id)


@router.post("/{report_id}/resolve", response_model=ReportRead)
def resolve_report(report_id: uuid.UUID, db: DBSession):
    return report_service.resolve_report(db, report_id)


@router.post("/{report_id}/dismiss", response_model=ReportRead)
def dismiss_report(report_id: uuid.UUID, db: DBSession):
    return report_service.dismiss_report(db, report_id)


