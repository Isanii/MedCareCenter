"""
patient.py

Quản lý hồ sơ bệnh nhân.

Quan hệ:

User 1 ----- 1 Patient

Patient 1 ----- N Appointment
"""

from datetime import date

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Unicode

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Patient(Base, TimestampMixin):
    """
    Bảng hồ sơ bệnh nhân.
    """

    __tablename__ = "patients"

    # Khóa chính
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Liên kết User
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True
    )

    # Ngày sinh
    birthday: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    # Giới tính
    gender: Mapped[str | None] = mapped_column(
        Unicode(20),
        nullable=True
    )

    # Địa chỉ
    address: Mapped[str | None] = mapped_column(
        Unicode(255),
        nullable=True
    )

    # ==========================
    # QUAN HỆ
    # ==========================

    user = relationship(
        "User",
        back_populates="patient"
    )

    appointments = relationship(
        "Appointment",
        back_populates="patient"
    )

    def __repr__(self):
        return (
            f"<Patient("
            f"id={self.id}, "
            f"user_id={self.user_id}"
            f")>"
        )