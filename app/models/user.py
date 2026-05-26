"""
user.py

Quản lý tài khoản người dùng.

Mỗi tài khoản có thể thuộc một trong các vai trò:

- admin
- receptionist
- doctor
- patient

Quan hệ:

User
 ├── Doctor (1-1)
 └── Patient (1-1)
"""

from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    """
    Bảng lưu thông tin tài khoản.

    Đây là bảng dùng cho đăng nhập và phân quyền.
    """

    __tablename__ = "users"

    # ==========================
    # KHÓA CHÍNH
    # ==========================

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # ==========================
    # THÔNG TIN CÁ NHÂN
    # ==========================

    fullname: Mapped[str] = mapped_column(
        Unicode(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    # ==========================
    # ĐĂNG NHẬP
    # ==========================

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # ==========================
    # PHÂN QUYỀN
    # ==========================

    role: Mapped[str] = mapped_column(
        String(30),
        default="patient"
    )

    # ==========================
    # TRẠNG THÁI
    # ==========================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # ==========================
    # QUAN HỆ
    # ==========================

    # Một User có thể là một Doctor
    doctor = relationship(
        "Doctor",
        back_populates="user",
        uselist=False
    )

    # Một User có thể là một Patient
    patient = relationship(
        "Patient",
        back_populates="user",
        uselist=False
    )

    def __repr__(self):
        return (
            f"<User("
            f"id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role}'"
            f")>"
        )