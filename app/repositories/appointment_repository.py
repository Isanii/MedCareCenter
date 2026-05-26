"""
appointment_repository.py

Repository quản lý lịch hẹn.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.appointment import Appointment


class AppointmentRepository:

    @staticmethod
    def create(
        db: Session,
        appointment: Appointment
    ) -> Appointment:

        db.add(appointment)

        db.commit()

        db.refresh(appointment)

        return appointment

    @staticmethod
    def get_by_id(
        db: Session,
        appointment_id: int
    ) -> Appointment | None:

        return (
            db.query(Appointment)
            .filter(
                Appointment.id == appointment_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session
    ) -> list[Appointment]:

        return (
            db.query(Appointment)
            .order_by(
                Appointment.id.desc()
            )
            .all()
        )

    @staticmethod
    def doctor_has_schedule(
        db: Session,
        doctor_id: int,
        appointment_time: datetime
    ) -> bool:
        """
        Kiểm tra bác sĩ có lịch trùng hay không.
        """

        existing = (
            db.query(Appointment)
            .filter(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_time == appointment_time
            )
            .first()
        )

        return existing is not None


    @staticmethod
    def update(
        db: Session,
        appointment: Appointment
    ) -> Appointment:
        """
        Cập nhật lịch hẹn.
        """

        db.commit()

        db.refresh(appointment)

        return appointment


    @staticmethod
    def get_by_patient(
        db: Session,
        patient_id: int
    ):
        """
        Danh sách lịch hẹn của bệnh nhân.
        """

        return (
            db.query(Appointment)
            .filter(
                Appointment.patient_id == patient_id
            )
            .all()
        )


    @staticmethod
    def get_by_doctor(
        db: Session,
        doctor_id: int
    ):
        """
        Danh sách lịch hẹn của bác sĩ.
        """

        return (
            db.query(Appointment)
            .filter(
                Appointment.doctor_id == doctor_id
            )
            .all()
        )