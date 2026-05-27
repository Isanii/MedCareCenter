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

class PatientCreateWithUser(BaseModel):
    fullname: str

    email: str

    phone: str

    password: str

    birthday: date | None = None

    gender: str | None = None

    address: str | None = None
    
class PatientResponse(BaseModel):
    id: int

    user_id: int

    fullname: str

    email: str

    phone: str | None

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