"""
appointment.py

Schema quản lý lịch hẹn khám bệnh.
"""

from datetime import datetime

from pydantic import BaseModel

from app.utils.constants import (AppointmentStatus)

class AppointmentCreate(BaseModel):
    """
    Tạo lịch hẹn mới.
    """

    patient_id: int

    doctor_id: int

    appointment_time: datetime

    note: str | None = None


class AppointmentResponse(BaseModel):
    """
    Thông tin lịch hẹn.
    """

    id: int

    patient_id: int

    doctor_id: int

    appointment_time: datetime

    status: str

    note: str | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class AppointmentUpdateStatus(
    BaseModel
):
    status: AppointmentStatus