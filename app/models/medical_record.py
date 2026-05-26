"""
medical_record.py

Quản lý bệnh án điện tử.

Được tạo sau khi bác sĩ khám bệnh.

Bao gồm:

- Triệu chứng
- Chẩn đoán
- Đơn thuốc
- Ghi chú bác sĩ
"""

from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import UnicodeText
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class MedicalRecord(Base, TimestampMixin):
    """
    Bảng bệnh án điện tử.
    """

    __tablename__ = "medical_records"

    # ==========================
    # KHÓA CHÍNH
    # ==========================

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # ==========================
    # KHÓA NGOẠI
    # ==========================

    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id"),
        unique=True
    )

    # ==========================
    # THÔNG TIN KHÁM BỆNH
    # ==========================

    symptoms: Mapped[str | None] = mapped_column(
        UnicodeText,
        nullable=True
    )

    diagnosis: Mapped[str | None] = mapped_column(
        UnicodeText,
        nullable=True
    )

    prescription: Mapped[str | None] = mapped_column(
        UnicodeText,
        nullable=True
    )

    doctor_note: Mapped[str | None] = mapped_column(
        UnicodeText,
        nullable=True
    )

    # ==========================
    # QUAN HỆ
    # ==========================

    appointment = relationship(
        "Appointment",
        back_populates="medical_record"
    )

    def __repr__(self):
        return (
            f"<MedicalRecord("
            f"id={self.id}"
            f")>"
        )