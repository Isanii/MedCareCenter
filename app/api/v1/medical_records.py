from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse
)

from app.services.medical_record_service import (
    MedicalRecordService
)

from app.dependencies.roles import (
    DoctorOrAdmin,
    PatientOnly
)

from app.dependencies.auth import (
    get_current_user
)

from app.models.user import (
    User
)
router = APIRouter(
    prefix="/api/v1/medical-records",
    tags=["Medical Records"]
)

# ==========================
# TẠO BỆNH ÁN
# ==========================

@router.post(
    "/",
    response_model=MedicalRecordResponse,
    dependencies=[Depends(DoctorOrAdmin)]
)
def create_record(
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


# ==========================
# DANH SÁCH BỆNH ÁN
# ==========================

@router.get(
    "/",
    response_model=list[
        MedicalRecordResponse
    ],
    dependencies=[
        Depends(
            DoctorOrAdmin
        )
    ]
)
def get_all(
    db: Session = Depends(
        get_db
    )
):
    return (
        MedicalRecordService
        .get_all(
            db
        )
    )

    
@router.get(
    "/my",
    response_model=list[
        MedicalRecordResponse
    ],
    dependencies=[
        Depends(PatientOnly)
    ]
)
def my_records(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    try:

        return (
            MedicalRecordService
            .get_my_records(
                db,
                current_user
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

# ==========================
# CHI TIẾT BỆNH ÁN
# ==========================

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


# ==========================
# TÌM THEO APPOINTMENT
# ==========================

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


# ==========================
# CẬP NHẬT BỆNH ÁN
# ==========================

@router.put(
    "/{record_id}",
    response_model=MedicalRecordResponse,
    dependencies=[
        Depends(DoctorOrAdmin)
    ]
)
def update_record(
    record_id: int,
    data: MedicalRecordUpdate,
    db: Session = Depends(get_db)
):
    try:

        return (
            MedicalRecordService
            .update_record(
                db,
                record_id,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ==========================
# XÓA BỆNH ÁN
# ==========================

@router.delete(
    "/{record_id}",
    dependencies=[
        Depends(DoctorOrAdmin)
    ]
)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    try:

        MedicalRecordService.delete_record(
            db,
            record_id
        )

        return {
            "message":
            "Xóa bệnh án thành công"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )