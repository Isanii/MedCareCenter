"""
medical_record_service.py

Xử lý nghiệp vụ bệnh án.
"""

from sqlalchemy.orm import Session

from app.models.medical_record import (
    MedicalRecord
)

from app.repositories.medical_record_repository import (
    MedicalRecordRepository
)

from app.repositories.appointment_repository import (
    AppointmentRepository
)

from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordUpdate
)


class MedicalRecordService:

    @staticmethod
    def create_record(
        db: Session,
        data: MedicalRecordCreate
    ):
        """
        Tạo bệnh án.
        """

        appointment = (
            AppointmentRepository
            .get_by_id(
                db,
                data.appointment_id
            )
        )

        if not appointment:
            raise ValueError(
                "Không tìm thấy lịch hẹn"
            )

        existing = (
            MedicalRecordRepository
            .get_by_appointment(
                db,
                data.appointment_id
            )
        )

        if existing:
            raise ValueError(
                "Lịch hẹn đã có bệnh án"
            )

        record = MedicalRecord(
            appointment_id=data.appointment_id,
            symptoms=data.symptoms,
            diagnosis=data.diagnosis,
            prescription=data.prescription,
            doctor_note=data.doctor_note
        )

        return (
            MedicalRecordRepository.create(
                db,
                record
            )
        )

    @staticmethod
    def get_record(
        db: Session,
        record_id: int
    ):
        record = (
            MedicalRecordRepository.get_by_id(
                db,
                record_id
            )
        )

        if not record:
            raise ValueError(
                "Không tìm thấy bệnh án"
            )

        return record

    @staticmethod
    def get_by_appointment(
        db: Session,
        appointment_id: int
    ):
        record = (
            MedicalRecordRepository
            .get_by_appointment(
                db,
                appointment_id
            )
        )

        if not record:
            raise ValueError(
                "Không tìm thấy bệnh án"
            )

        return record

    @staticmethod
    def get_all(
        db: Session
    ):
        return (
            MedicalRecordRepository
            .get_all(db)
        )