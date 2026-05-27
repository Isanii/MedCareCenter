"""
patient_service.py

Xử lý nghiệp vụ bệnh nhân.
"""

from sqlalchemy.orm import Session

from app.models.patient import Patient

from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientCreateWithUser
)
from app.models.user import User

from app.core.security import (
    hash_password
)

from app.utils.constants import (
    UserRole
)

from app.repositories.patient_repository import (
    PatientRepository
)

from app.repositories.user_repository import (
    UserRepository
)
from app.models.appointment import (
    Appointment
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
        db: Session,
        skip: int = 0,
        limit: int = 20
    ):
        """
        Lấy danh sách bệnh nhân có phân trang.
        """

        return PatientRepository.get_all(
            db,
            skip,
            limit
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

        has_appointments = (
            db.query(
                Appointment
            )
            .filter(
                Appointment.patient_id
                == patient_id
            )
            .first()
        )

        if has_appointments:

            raise ValueError(
                "Không thể xóa bệnh nhân đã có lịch khám"
            )

        PatientRepository.delete(
            db,
            patient
        )
    @staticmethod
    def search(
        db: Session,
        keyword: str
    ):
        return (
            PatientRepository.search(
                db,
                keyword
            )
        )


    @staticmethod
    def create_patient_with_user(
        db: Session,
        data: PatientCreateWithUser
    ):
        """
        Tạo User + Patient.
        """

        existing = UserRepository.get_by_email(
            db,
            data.email
        )

        if existing:
            raise ValueError(
                "Email đã tồn tại"
            )

        user = User(
            fullname=data.fullname,
            email=data.email,
            phone=data.phone,
            role=UserRole.PATIENT,
            hashed_password=hash_password(
                data.password
            )
        )

        db.add(user)

        db.flush()

        patient = Patient(
            user_id=user.id,
            birthday=data.birthday,
            gender=data.gender,
            address=data.address
        )

        db.add(patient)

        db.commit()

        db.refresh(patient)

        return patient