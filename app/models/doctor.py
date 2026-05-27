"""
doctor.py

Quản lý thông tin chuyên môn của bác sĩ.

Quan hệ:

User 1 ----- 1 Doctor

Doctor 1 ----- N Appointment
"""

from sqlalchemy import ForeignKey
from sqlalchemy import Unicode

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Doctor(Base, TimestampMixin):
    """
    Bảng thông tin bác sĩ.
    """

    __tablename__ = "doctors"

    # Khóa chính
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # Liên kết tới bảng User
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True
    )

    # Chuyên khoa
    specialty: Mapped[str] = mapped_column(
        Unicode(100)
    )

    # Phòng khám
    room_number: Mapped[str | None] = mapped_column(
        Unicode(50),
        nullable=True
    )

    # Số năm kinh nghiệm
    years_of_experience: Mapped[int] = mapped_column(
        default=0
    )

    # ==========================
    # QUAN HỆ
    # ==========================

    user = relationship(
        "User",
        back_populates="doctor"
    )

    @property
    def fullname(self):
        return self.user.fullname


    @property
    def email(self):
        return self.user.email
        
    appointments = relationship(
        "Appointment",
        back_populates="doctor"
    )

    def __repr__(self):
        return (
            f"<Doctor("
            f"id={self.id}, "
            f"specialty='{self.specialty}'"
            f")>"
        )