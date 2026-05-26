"""
patient.py

Schema quản lý bệnh nhân.
"""

from datetime import date
from datetime import datetime

from pydantic import BaseModel


class PatientCreate(BaseModel):
    """
    Tạo hồ sơ bệnh nhân.
    """

    user_id: int

    birthday: date | None = None

    gender: str | None = None

    address: str | None = None


class PatientResponse(BaseModel):
    """
    Thông tin bệnh nhân.
    """

    id: int

    user_id: int

    birthday: date | None

    gender: str | None

    address: str | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class PatientUpdate(BaseModel):
    """
    Cập nhật hồ sơ bệnh nhân.
    """

    birthday: date | None = None

    gender: str | None = None

    address: str | None = None