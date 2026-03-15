"""Catalog routers for master lookup tables.

These endpoints serve all the reference data (amenities, activities, languages,
certifications, dining options, safety features, insurance options, house rules,
equipment, and treatment services) that listings can reference.
"""
from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import DBSession, PaginationParams, http_bearer
from src.crud.crud_activity import crud_activity
from src.crud.crud_amenity import crud_amenity
from src.crud.crud_certification import crud_certification
from src.crud.crud_dining import crud_dining_option
from src.crud.crud_equipment import crud_equipment
from src.crud.crud_house_rule import crud_house_rule
from src.crud.crud_insurance import crud_insurance_option
from src.crud.crud_language import crud_language
from src.crud.crud_safety import crud_safety_feature
from src.crud.crud_service import crud_treatment_service
from src.schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate
from src.schemas.amenity import AmenityCreate, AmenityRead, AmenityUpdate
from src.schemas.certification import CertificationCreate, CertificationRead, CertificationUpdate
from src.schemas.dining import DiningOptionCreate, DiningOptionRead, DiningOptionUpdate
from src.schemas.equipment import EquipmentCreate, EquipmentRead, EquipmentUpdate
from src.schemas.house_rule import HouseRuleCreate, HouseRuleRead, HouseRuleUpdate
from src.schemas.insurance import InsuranceOptionCreate, InsuranceOptionRead, InsuranceOptionUpdate
from src.schemas.language import LanguageCreate, LanguageRead, LanguageUpdate
from src.schemas.safety import SafetyFeatureCreate, SafetyFeatureRead, SafetyFeatureUpdate
from src.schemas.service import TreatmentServiceCreate, TreatmentServiceRead, TreatmentServiceUpdate

# ── Amenities ──────────────────────────────────────────────────────────────────

amenities_router = APIRouter(prefix="/amenities", tags=["Catalog – Amenities"])


@amenities_router.get("/", response_model=List[AmenityRead])
def list_amenities(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_amenity.get_all(db, skip=skip, limit=limit)


@amenities_router.get("/{amenity_id}", response_model=AmenityRead)
def get_amenity(amenity_id: uuid.UUID, db: DBSession):
    obj = crud_amenity.get_by_id(db, amenity_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Amenity not found")
    return obj


@amenities_router.post("/", response_model=AmenityRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_amenity(payload: AmenityCreate, db: DBSession):
    return crud_amenity.create(db, payload)


@amenities_router.put("/{amenity_id}", response_model=AmenityRead, dependencies=[Depends(http_bearer)])
def update_amenity(amenity_id: uuid.UUID, payload: AmenityUpdate, db: DBSession):
    obj = crud_amenity.get_by_id(db, amenity_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Amenity not found")
    return crud_amenity.update(db, obj, payload)


@amenities_router.delete("/{amenity_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_amenity(amenity_id: uuid.UUID, db: DBSession):
    if crud_amenity.delete(db, amenity_id) is None:
        raise HTTPException(status_code=404, detail="Amenity not found")


# ── Activities ────────────────────────────────────────────────────────────────

activities_router = APIRouter(prefix="/activities", tags=["Catalog – Activities"])


@activities_router.get("/", response_model=List[ActivityRead])
def list_activities(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_activity.get_all(db, skip=skip, limit=limit)


@activities_router.get("/{activity_id}", response_model=ActivityRead)
def get_activity(activity_id: uuid.UUID, db: DBSession):
    obj = crud_activity.get_by_id(db, activity_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return obj


@activities_router.post("/", response_model=ActivityRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_activity(payload: ActivityCreate, db: DBSession):
    return crud_activity.create(db, payload)


@activities_router.put("/{activity_id}", response_model=ActivityRead, dependencies=[Depends(http_bearer)])
def update_activity(activity_id: uuid.UUID, payload: ActivityUpdate, db: DBSession):
    obj = crud_activity.get_by_id(db, activity_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return crud_activity.update(db, obj, payload)


@activities_router.delete("/{activity_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_activity(activity_id: uuid.UUID, db: DBSession):
    if crud_activity.delete(db, activity_id) is None:
        raise HTTPException(status_code=404, detail="Activity not found")


# ── Languages ─────────────────────────────────────────────────────────────────

languages_router = APIRouter(prefix="/languages", tags=["Catalog – Languages"])


@languages_router.get("/", response_model=List[LanguageRead])
def list_languages(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_language.get_all(db, skip=skip, limit=limit)


@languages_router.post("/", response_model=LanguageRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_language(payload: LanguageCreate, db: DBSession):
    return crud_language.create(db, payload)


@languages_router.put("/{language_id}", response_model=LanguageRead, dependencies=[Depends(http_bearer)])
def update_language(language_id: uuid.UUID, payload: LanguageUpdate, db: DBSession):
    obj = crud_language.get_by_id(db, language_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return crud_language.update(db, obj, payload)


@languages_router.delete("/{language_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_language(language_id: uuid.UUID, db: DBSession):
    if crud_language.delete(db, language_id) is None:
        raise HTTPException(status_code=404, detail="Language not found")


# ── Certifications ────────────────────────────────────────────────────────────

certifications_router = APIRouter(prefix="/certifications", tags=["Catalog – Certifications"])


@certifications_router.get("/", response_model=List[CertificationRead])
def list_certifications(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_certification.get_all(db, skip=skip, limit=limit)


@certifications_router.post("/", response_model=CertificationRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_certification(payload: CertificationCreate, db: DBSession):
    return crud_certification.create(db, payload)


@certifications_router.put("/{cert_id}", response_model=CertificationRead, dependencies=[Depends(http_bearer)])
def update_certification(cert_id: uuid.UUID, payload: CertificationUpdate, db: DBSession):
    obj = crud_certification.get_by_id(db, cert_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Certification not found")
    return crud_certification.update(db, obj, payload)


@certifications_router.delete("/{cert_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_certification(cert_id: uuid.UUID, db: DBSession):
    if crud_certification.delete(db, cert_id) is None:
        raise HTTPException(status_code=404, detail="Certification not found")


# ── Dining Options ────────────────────────────────────────────────────────────

dining_router = APIRouter(prefix="/dining-options", tags=["Catalog – Dining Options"])


@dining_router.get("/", response_model=List[DiningOptionRead])
def list_dining_options(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_dining_option.get_all(db, skip=skip, limit=limit)


@dining_router.post("/", response_model=DiningOptionRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_dining_option(payload: DiningOptionCreate, db: DBSession):
    return crud_dining_option.create(db, payload)


@dining_router.put("/{dining_id}", response_model=DiningOptionRead, dependencies=[Depends(http_bearer)])
def update_dining_option(dining_id: uuid.UUID, payload: DiningOptionUpdate, db: DBSession):
    obj = crud_dining_option.get_by_id(db, dining_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Dining option not found")
    return crud_dining_option.update(db, obj, payload)


@dining_router.delete("/{dining_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_dining_option(dining_id: uuid.UUID, db: DBSession):
    if crud_dining_option.delete(db, dining_id) is None:
        raise HTTPException(status_code=404, detail="Dining option not found")


# ── Safety Features ───────────────────────────────────────────────────────────

safety_router = APIRouter(prefix="/safety-features", tags=["Catalog – Safety Features"])


@safety_router.get("/", response_model=List[SafetyFeatureRead])
def list_safety_features(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_safety_feature.get_all(db, skip=skip, limit=limit)


@safety_router.post("/", response_model=SafetyFeatureRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_safety_feature(payload: SafetyFeatureCreate, db: DBSession):
    return crud_safety_feature.create(db, payload)


@safety_router.put("/{sf_id}", response_model=SafetyFeatureRead, dependencies=[Depends(http_bearer)])
def update_safety_feature(sf_id: uuid.UUID, payload: SafetyFeatureUpdate, db: DBSession):
    obj = crud_safety_feature.get_by_id(db, sf_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Safety feature not found")
    return crud_safety_feature.update(db, obj, payload)


@safety_router.delete("/{sf_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_safety_feature(sf_id: uuid.UUID, db: DBSession):
    if crud_safety_feature.delete(db, sf_id) is None:
        raise HTTPException(status_code=404, detail="Safety feature not found")


# ── Insurance Options ─────────────────────────────────────────────────────────

insurance_router = APIRouter(prefix="/insurance-options", tags=["Catalog – Insurance Options"])


@insurance_router.get("/", response_model=List[InsuranceOptionRead])
def list_insurance_options(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_insurance_option.get_all(db, skip=skip, limit=limit)


@insurance_router.post("/", response_model=InsuranceOptionRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_insurance_option(payload: InsuranceOptionCreate, db: DBSession):
    return crud_insurance_option.create(db, payload)


@insurance_router.put("/{ins_id}", response_model=InsuranceOptionRead, dependencies=[Depends(http_bearer)])
def update_insurance_option(ins_id: uuid.UUID, payload: InsuranceOptionUpdate, db: DBSession):
    obj = crud_insurance_option.get_by_id(db, ins_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Insurance option not found")
    return crud_insurance_option.update(db, obj, payload)


@insurance_router.delete("/{ins_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_insurance_option(ins_id: uuid.UUID, db: DBSession):
    if crud_insurance_option.delete(db, ins_id) is None:
        raise HTTPException(status_code=404, detail="Insurance option not found")


# ── House Rules ───────────────────────────────────────────────────────────────

house_rules_router = APIRouter(prefix="/house-rules", tags=["Catalog – House Rules"])


@house_rules_router.get("/", response_model=List[HouseRuleRead])
def list_house_rules(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_house_rule.get_all(db, skip=skip, limit=limit)


@house_rules_router.post("/", response_model=HouseRuleRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_house_rule(payload: HouseRuleCreate, db: DBSession):
    return crud_house_rule.create(db, payload)


@house_rules_router.put("/{hr_id}", response_model=HouseRuleRead, dependencies=[Depends(http_bearer)])
def update_house_rule(hr_id: uuid.UUID, payload: HouseRuleUpdate, db: DBSession):
    obj = crud_house_rule.get_by_id(db, hr_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="House rule not found")
    return crud_house_rule.update(db, obj, payload)


@house_rules_router.delete("/{hr_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_house_rule(hr_id: uuid.UUID, db: DBSession):
    if crud_house_rule.delete(db, hr_id) is None:
        raise HTTPException(status_code=404, detail="House rule not found")


# ── Equipment ─────────────────────────────────────────────────────────────────

equipment_router = APIRouter(prefix="/equipment", tags=["Catalog – Equipment"])


@equipment_router.get("/", response_model=List[EquipmentRead])
def list_equipment(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_equipment.get_all(db, skip=skip, limit=limit)


@equipment_router.post("/", response_model=EquipmentRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_equipment(payload: EquipmentCreate, db: DBSession):
    return crud_equipment.create(db, payload)


@equipment_router.put("/{eq_id}", response_model=EquipmentRead, dependencies=[Depends(http_bearer)])
def update_equipment(eq_id: uuid.UUID, payload: EquipmentUpdate, db: DBSession):
    obj = crud_equipment.get_by_id(db, eq_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return crud_equipment.update(db, obj, payload)


@equipment_router.delete("/{eq_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_equipment(eq_id: uuid.UUID, db: DBSession):
    if crud_equipment.delete(db, eq_id) is None:
        raise HTTPException(status_code=404, detail="Equipment not found")


# ── Treatment Services ────────────────────────────────────────────────────────

services_router = APIRouter(prefix="/treatment-services", tags=["Catalog – Treatment Services"])


@services_router.get("/", response_model=List[TreatmentServiceRead])
def list_treatment_services(db: DBSession, pagination: PaginationParams):
    skip, limit = pagination
    return crud_treatment_service.get_all(db, skip=skip, limit=limit)


@services_router.post("/", response_model=TreatmentServiceRead, status_code=201, dependencies=[Depends(http_bearer)])
def create_treatment_service(payload: TreatmentServiceCreate, db: DBSession):
    return crud_treatment_service.create(db, payload)


@services_router.put("/{ts_id}", response_model=TreatmentServiceRead, dependencies=[Depends(http_bearer)])
def update_treatment_service(
    ts_id: uuid.UUID, payload: TreatmentServiceUpdate, db: DBSession
):
    obj = crud_treatment_service.get_by_id(db, ts_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Treatment service not found")
    return crud_treatment_service.update(db, obj, payload)


@services_router.delete("/{ts_id}", status_code=204, dependencies=[Depends(http_bearer)])
def delete_treatment_service(ts_id: uuid.UUID, db: DBSession):
    if crud_treatment_service.delete(db, ts_id) is None:
        raise HTTPException(status_code=404, detail="Treatment service not found")


