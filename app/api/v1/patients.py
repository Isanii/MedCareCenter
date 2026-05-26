"""
patients.py

API quản lý bệnh nhân.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.patient_service import (
    PatientService
)

from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse
)

router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"]
)

#Danh sách bệnh nhân
@router.get(
    "/",
    response_model=list[PatientResponse]
)
def get_all_patients(
    db: Session = Depends(get_db)
):
    return (
        PatientService.get_all_patients(
            db
        )
    )

#Chi tiết bệnh nhân
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    try:

        return (
            PatientService.get_patient(
                db,
                patient_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

#Tạo bệnh nhân
@router.post(
    "/",
    response_model=PatientResponse
)
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db)
):
    try:

        return (
            PatientService.create_patient(
                db,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )