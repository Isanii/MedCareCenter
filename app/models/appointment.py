"""
appointment.py

Quản lý lịch hẹn khám bệnh.

Vai trò:

- Bệnh nhân tạo lịch hẹn
- Lễ tân xác nhận lịch
- Bác sĩ tiếp nhận khám

Quan hệ:

Patient 1 ----- N Appointment

Doctor 1 ----- N Appointment

Appointment 1 ----- 1 MedicalRecord

Appointment 1 ----- 1 Invoice
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UnicodeText

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Appointment(Base, TimestampMixin):
    """
    Bảng lịch hẹn khám bệnh.
    """

    __tablename__ = "appointments"

    # ==========================
    # KHÓA CHÍNH
    # ==========================

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # ==========================
    # KHÓA NGOẠI
    # ==========================

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id"),
        nullable=False
    )

    # ==========================
    # THÔNG TIN LỊCH HẸN
    # ==========================

    appointment_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    note: Mapped[str | None] = mapped_column(
        UnicodeText,
        nullable=True
    )

    # ==========================
    # TRẠNG THÁI
    # ==========================

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending"
    )

    # ==========================
    # QUAN HỆ
    # ==========================

    patient = relationship(
        "Patient",
        back_populates="appointments"
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments"
    )
    
    @property
    def patient_name(self):
        return self.patient.fullname


    @property
    def doctor_name(self):
        return self.doctor.fullname

    medical_record = relationship(
        "MedicalRecord",
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan"
    )

    invoice = relationship(
        "Invoice",
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Appointment("
            f"id={self.id}, "
            f"status='{self.status}'"
            f")>"
        )