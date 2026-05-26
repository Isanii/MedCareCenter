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
    """
    Thông tin bác sĩ.
    """

    id: int

    user_id: int

    specialty: str

    room_number: str | None

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