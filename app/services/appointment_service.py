from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.user import User

from app.schemas.appointment import (
    AppointmentCreate,
    PatientAppointmentCreate
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
    def get_all_appointments(
        db: Session,
        skip: int = 0,
        limit: int = 20
    ):
        return (
            AppointmentRepository.get_all(
                db,
                skip,
                limit
            )
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

    @staticmethod
    def get_my_appointments(
        db: Session,
        current_user: User
    ):
        patient = (
            PatientRepository
            .get_by_user_id(
                db,
                current_user.id
            )
        )

        if not patient:
            raise ValueError(
                "Không tìm thấy hồ sơ bệnh nhân"
            )

        return (
            AppointmentRepository
            .get_by_patient_id(
                db,
                patient.id
            )
        )

    @staticmethod
    def create_my_appointment(
        db: Session,
        current_user: User,
        data: PatientAppointmentCreate
    ):
        patient = (
            PatientRepository
            .get_by_user_id(
                db,
                current_user.id
            )
        )

        if not patient:
            raise ValueError(
                "Không tìm thấy hồ sơ bệnh nhân"
            )

        doctor = (
            DoctorRepository
            .get_by_id(
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
            patient_id=patient.id,
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
    def get_doctor_appointments(
        db: Session,
        current_user: User
    ):
        doctor = (
            DoctorRepository
            .get_by_user_id(
                db,
                current_user.id
            )
        )

        if not doctor:

            raise ValueError(
                "Không tìm thấy bác sĩ"
            )

        return (
            AppointmentRepository
            .get_by_doctor_id(
                db,
                doctor.id
            )
        )