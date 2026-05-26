from sqlalchemy.orm import Session

from app.models.appointment import Appointment

from app.schemas.appointment import (
    AppointmentCreate
)

from app.repositories.appointment_repository import (
    AppointmentRepository
)

from app.repositories.patient_repository import (
    PatientRepository
)

from app.repositories.doctor_repository import (
    DoctorRepository
)


class AppointmentService:

    @staticmethod
    def create_appointment(
        db: Session,
        data: AppointmentCreate
    ):
        patient = (
            PatientRepository.get_by_id(
                db,
                data.patient_id
            )
        )

        if not patient:
            raise ValueError(
                "Không tìm thấy bệnh nhân"
            )

        doctor = (
            DoctorRepository.get_by_id(
                db,
                data.doctor_id
            )
        )

        if not doctor:
            raise ValueError(
                "Không tìm thấy bác sĩ"
            )

        busy = (
            AppointmentRepository
            .doctor_has_schedule(
                db,
                data.doctor_id,
                data.appointment_time
            )
        )

        if busy:
            raise ValueError(
                "Bác sĩ đã có lịch khám"
            )

        appointment = Appointment(
            patient_id=data.patient_id,
            doctor_id=data.doctor_id,
            appointment_time=data.appointment_time,
            note=data.note,
            status="pending"
        )

        return AppointmentRepository.create(
            db,
            appointment
        )

    @staticmethod
    def get_all(
        db: Session
    ):
        return AppointmentRepository.get_all(
            db
        )

    @staticmethod
    def get_appointment(
        db: Session,
        appointment_id: int
    ):
        appointment = (
            AppointmentRepository.get_by_id(
                db,
                appointment_id
            )
        )

        if not appointment:
            raise ValueError(
                "Không tìm thấy lịch hẹn"
            )

        return appointment

    @staticmethod
    def update_status(
        db: Session,
        appointment_id: int,
        status: str
    ):
        appointment = (
            AppointmentRepository.get_by_id(
                db,
                appointment_id
            )
        )

        if not appointment:
            raise ValueError(
                "Không tìm thấy lịch hẹn"
            )

        appointment.status = status

        return AppointmentRepository.update(
            db,
            appointment
        )