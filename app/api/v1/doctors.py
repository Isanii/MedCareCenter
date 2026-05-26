"""
doctors.py

API quản lý bác sĩ.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.doctor_service import (
    DoctorService
)

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse
)

router = APIRouter(
    prefix="/api/v1/doctors",
    tags=["Doctors"]
)

#API Lấy Danh Sách
@router.get(
    "/",
    response_model=list[DoctorResponse]
)
def get_all_doctors(
    db: Session = Depends(get_db)
):
    """
    Danh sách bác sĩ.
    """

    return (
        DoctorService.get_all_doctors(
            db
        )
    )


@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """
    Chi tiết bác sĩ.
    """

    try:

        return (
            DoctorService.get_doctor(
                db,
                doctor_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

#API Tạo bác sĩ
@router.post(
    "/",
    response_model=DoctorResponse
)
def create_doctor(
    data: DoctorCreate,
    db: Session = Depends(get_db)
):
    """
    Tạo bác sĩ mới.
    """

    try:

        return (
            DoctorService.create_doctor(
                db,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )