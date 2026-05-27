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
    PatientAppointmentCreate,
    AppointmentResponse,
    AppointmentUpdateStatus
)

from app.dependencies.auth import (
    get_current_user
)

from app.models.user import User

from app.dependencies.roles import (
    AdminOnly,
    PatientOnly,
    DoctorOnly,
    ReceptionOrAdmin
)

router = APIRouter(
    prefix="/api/v1/appointments",
    tags=["Appointments"]
)


# ==========================
# ADMIN TẠO LỊCH HẸN
# ==========================

@router.post(
    "/",
    response_model=AppointmentResponse,
    dependencies=[Depends(AdminOnly)],
    status_code=201,
    summary="Admin tạo lịch hẹn"
)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db)
):
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


# ==========================
# PATIENT TỰ ĐẶT LỊCH
# ==========================

@router.post(
    "/my",
    response_model=AppointmentResponse,
    dependencies=[Depends(PatientOnly)],
    status_code=201,
    summary="Bệnh nhân tự đặt lịch"
)
def create_my_appointment(
    data: PatientAppointmentCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    try:

        return (
            AppointmentService
            .create_my_appointment(
                db,
                current_user,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ==========================
# DANH SÁCH LỊCH HẸN
# ==========================

@router.get(
    "/",
    response_model=list[
        AppointmentResponse
    ],
    dependencies=[
        Depends(
            ReceptionOrAdmin
        )
    ]
)
def get_appointments(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(
        get_db
    )
):
    return (
        AppointmentService
        .get_all_appointments(
            db,
            skip,
            limit
        )
    )

# ==========================
# LỊCH HẸN CỦA TÔI
# ==========================

@router.get(
    "/my",
    response_model=list[
        AppointmentResponse
    ]
)
def my_appointments(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    try:

        return (
            AppointmentService
            .get_my_appointments(
                db,
                current_user
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.get(
    "/my-doctor",
    response_model=list[
        AppointmentResponse
    ],
    dependencies=[
        Depends(DoctorOnly)
    ]
)
def my_doctor_appointments(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    try:

        return (
            AppointmentService
            .get_doctor_appointments(
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
# CHI TIẾT LỊCH HẸN
# ==========================

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
            AppointmentService
            .get_appointment(
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
# CẬP NHẬT TRẠNG THÁI
# ==========================

@router.patch(
    "/{appointment_id}/status",
    response_model=AppointmentResponse,
    summary="Cập nhật trạng thái lịch hẹn"
)
def update_status(
    appointment_id: int,
    data: AppointmentUpdateStatus,
    db: Session = Depends(get_db)
):
    try:

        return (
            AppointmentService
            .update_status(
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