"""
patient_service.py

Xử lý nghiệp vụ bệnh nhân.
"""

from sqlalchemy.orm import Session

from app.models.patient import Patient

from app.schemas.patient import (
    PatientCreate,
    PatientUpdate
)

from app.repositories.patient_repository import (
    PatientRepository
)

from app.repositories.user_repository import (
    UserRepository
)


class PatientService:

    @staticmethod
    def create_patient(
        db: Session,
        data: PatientCreate
    ):
        """
        Tạo hồ sơ bệnh nhân.
        """

        user = UserRepository.get_by_id(
            db,
            data.user_id
        )

        if not user:
            raise ValueError(
                "Không tìm thấy tài khoản"
            )

        existing = (
            PatientRepository.get_by_user_id(
                db,
                data.user_id
            )
        )

        if existing:
            raise ValueError(
                "Bệnh nhân đã tồn tại"
            )

        patient = Patient(
            user_id=data.user_id,
            birthday=data.birthday,
            gender=data.gender,
            address=data.address
        )

        return PatientRepository.create(
            db,
            patient
        )

    @staticmethod
    def get_all_patients(
        db: Session
    ):
        return PatientRepository.get_all(
            db
        )

    @staticmethod
    def get_patient(
        db: Session,
        patient_id: int
    ):
        patient = (
            PatientRepository.get_by_id(
                db,
                patient_id
            )
        )

        if not patient:
            raise ValueError(
                "Không tìm thấy bệnh nhân"
            )

        return patient

    @staticmethod
    def update_patient(
        db: Session,
        patient_id: int,
        data: PatientUpdate
    ):
        patient = (
            PatientRepository.get_by_id(
                db,
                patient_id
            )
        )

        if not patient:
            raise ValueError(
                "Không tìm thấy bệnh nhân"
            )

        if data.birthday is not None:
            patient.birthday = data.birthday

        if data.gender is not None:
            patient.gender = data.gender

        if data.address is not None:
            patient.address = data.address

        return PatientRepository.update(
            db,
            patient
        )

    @staticmethod
    def delete_patient(
        db: Session,
        patient_id: int
    ):
        patient = (
            PatientRepository.get_by_id(
                db,
                patient_id
            )
        )

        if not patient:
            raise ValueError(
                "Không tìm thấy bệnh nhân"
            )

        PatientRepository.delete(
            db,
            patient
        )