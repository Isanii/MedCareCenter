"""
appointments.py

API quản lý lịch hẹn khám bệnh.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.appointment_service import (
    AppointmentService
)

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdateStatus
)

from app.dependencies.roles import (
    PatientOnly
)

router = APIRouter(
    prefix="/api/v1/appointments",
    tags=["Appointments"]
)

#Tạo lịch hẹn

@router.post(
    "/",
    response_model=AppointmentResponse,
    dependencies=[Depends(PatientOnly)]
)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """
    Đặt lịch khám.
    """

    try:

        return (
            AppointmentService.create_appointment(
                db,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

#Danh sách lịch hẹn
@router.get(
    "/",
    response_model=list[AppointmentResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return AppointmentService.get_all(
        db
    )


#Chi tiết lịch hẹn
@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    try:

        return (
            AppointmentService.get_appointment(
                db,
                appointment_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

#Cập nhật trạng thái
@router.patch(
    "/{appointment_id}/status",
    response_model=AppointmentResponse
)
def update_status(
    appointment_id: int,
    data: AppointmentUpdateStatus,
    db: Session = Depends(get_db)
):
    try:

        return (
            AppointmentService.update_status(
                db,
                appointment_id,
                data.status
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )