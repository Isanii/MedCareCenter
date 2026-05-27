"""
doctor.py

Schema quản lý bác sĩ.
"""

from datetime import datetime

from pydantic import BaseModel


class DoctorCreate(BaseModel):
    """
    Tạo hồ sơ bác sĩ.
    """

    user_id: int

    specialty: str

    room_number: str | None = None

    years_of_experience: int = 0


class DoctorResponse(BaseModel):
    id: int
    user_id: int

    fullname: str
    email: str

    specialty: str
    room_number: str
    years_of_experience: int

    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class DoctorUpdate(BaseModel):
    """
    Cập nhật thông tin bác sĩ.
    """

    specialty: str | None = None

    room_number: str | None = None

    years_of_experience: int | None = None


class DoctorCreateWithUser(BaseModel):
    fullname: str

    email: str

    phone: str

    password: str

    specialty: str

    room_number: str | None = None

    years_of_experience: int = 0