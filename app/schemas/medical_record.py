from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class MedicalRecordCreate(
    BaseModel
):
    """
    Tạo bệnh án.
    """

    appointment_id: int

    symptoms: str

    diagnosis: str

    prescription: str

    doctor_note: str | None = None


class MedicalRecordUpdate(
    BaseModel
):
    """
    Cập nhật bệnh án.
    """

    symptoms: str | None = None

    diagnosis: str | None = None

    prescription: str | None = None

    doctor_note: str | None = None


class MedicalRecordResponse(
    BaseModel
):
    """
    Thông tin bệnh án.
    """

    id: int

    appointment_id: int

    symptoms: str | None

    diagnosis: str | None

    prescription: str | None

    doctor_note: str | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )