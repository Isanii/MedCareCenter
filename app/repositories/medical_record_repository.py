"""
medical_record_repository.py

Repository thao tác dữ liệu bệnh án.
"""

from sqlalchemy.orm import Session

from app.models.medical_record import (
    MedicalRecord
)

from app.models.appointment import (
    Appointment
)
class MedicalRecordRepository:

    @staticmethod
    def create(
        db: Session,
        record: MedicalRecord
    ) -> MedicalRecord:
        """
        Tạo bệnh án.
        """

        db.add(record)

        db.commit()

        db.refresh(record)

        return record

    @staticmethod
    def get_by_id(
        db: Session,
        record_id: int
    ) -> MedicalRecord | None:
        """
        Tìm bệnh án theo ID.
        """

        return (
            db.query(MedicalRecord)
            .filter(
                MedicalRecord.id == record_id
            )
            .first()
        )

    @staticmethod
    def get_by_appointment(
        db: Session,
        appointment_id: int
    ) -> MedicalRecord | None:
        """
        Tìm bệnh án theo lịch hẹn.
        """

        return (
            db.query(MedicalRecord)
            .filter(
                MedicalRecord.appointment_id
                == appointment_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session
    ):
        """
        Danh sách bệnh án.
        """

        return (
            db.query(MedicalRecord)
            .order_by(
                MedicalRecord.id.desc()
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        record: MedicalRecord
    ) -> MedicalRecord:

        db.commit()

        db.refresh(record)

        return record

    @staticmethod
    def delete(
        db: Session,
        record: MedicalRecord
    ):

        db.delete(record)

        db.commit()


    @staticmethod
    def get_by_patient_id(
        db: Session,
        patient_id: int
    ):
        """
        Danh sách bệnh án của bệnh nhân.
        """

        return (
            db.query(MedicalRecord)
            .join(
                Appointment,
                MedicalRecord.appointment_id
                ==
                Appointment.id
            )
            .filter(
                Appointment.patient_id
                ==
                patient_id
            )
            .order_by(
                MedicalRecord.id.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_doctor_id(
        db: Session,
        doctor_id: int
    ):
        return (
            db.query(MedicalRecord)
            .join(
                Appointment,
                MedicalRecord.appointment_id
                ==
                Appointment.id
            )
            .filter(
                Appointment.doctor_id
                ==
                doctor_id
            )
            .all()
        )