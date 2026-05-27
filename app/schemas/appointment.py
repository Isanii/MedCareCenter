"""
appointment.py

Schema quản lý lịch hẹn khám bệnh.
"""

from datetime import datetime

from pydantic import BaseModel

from app.utils.constants import (
    AppointmentStatus
)


class AppointmentCreate(
    BaseModel
):
    """
    Admin tạo lịch hẹn.
    """

    patient_id: int

    doctor_id: int

    appointment_time: datetime

    note: str | None = None


class PatientAppointmentCreate(
    BaseModel
):
    """
    Bệnh nhân tự đặt lịch.
    """

    doctor_id: int

    appointment_time: datetime

    note: str | None = None


class AppointmentResponse(
    BaseModel
):
    """
    Thông tin lịch hẹn.
    """

    id: int

    patient_id: int

    doctor_id: int

    patient_name: str

    doctor_name: str

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
    """
    Cập nhật trạng thái lịch hẹn.
    """

    status: AppointmentStatus