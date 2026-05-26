"""
base.py

Chứa các lớp dùng chung cho toàn bộ hệ thống.

Hiện tại gồm:

- TimestampMixin:
    Tự động quản lý thời gian tạo và cập nhật dữ liệu.
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class TimestampMixin:
    """
    Lớp dùng chung để thêm thông tin thời gian.

    Khi một bảng kế thừa lớp này sẽ tự động có:

    - created_at : thời gian tạo bản ghi
    - updated_at : thời gian cập nhật gần nhất
    """

    # Thời gian tạo dữ liệu
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Thời gian cập nhật dữ liệu
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )