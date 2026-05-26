from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordResponse
)

from app.services.medical_record_service import (
    MedicalRecordService
)

from app.dependencies.roles import (
    DoctorOnly
)

router = APIRouter(
    prefix="/api/v1/medical-records",
    tags=["Medical Records"]
)

#Tạo bệnh án
@router.post(
    "/",
    response_model=MedicalRecordResponse
)
def create_record(
    _ = DoctorOnly,
    data: MedicalRecordCreate,
    db: Session = Depends(get_db)
):
    try:

        return (
            MedicalRecordService
            .create_record(
                db,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

#Danh sách bệnh án
@router.get(
    "/",
    response_model=list[
        MedicalRecordResponse
    ]
)
def get_all(
    db: Session = Depends(get_db)
):
    return (
        MedicalRecordService
        .get_all(db)
    )

#Chi tiết bệnh án
@router.get(
    "/{record_id}",
    response_model=MedicalRecordResponse
)
def get_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    try:

        return (
            MedicalRecordService
            .get_record(
                db,
                record_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.get(
    "/appointment/{appointment_id}",
    response_model=MedicalRecordResponse
)
def get_by_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    try:

        return (
            MedicalRecordService
            .get_by_appointment(
                db,
                appointment_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )