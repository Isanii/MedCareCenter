"""
doctor_service.py

Xử lý nghiệp vụ bác sĩ.
"""

from sqlalchemy.orm import Session

from app.models.doctor import Doctor

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate
)

from app.repositories.doctor_repository import (
    DoctorRepository
)

from app.repositories.user_repository import (
    UserRepository
)


class DoctorService:
    """
    Service xử lý nghiệp vụ bác sĩ.
    """

    @staticmethod
    def create_doctor(
        db: Session,
        data: DoctorCreate
    ):
        """
        Tạo hồ sơ bác sĩ.
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
            DoctorRepository.get_by_user_id(
                db,
                data.user_id
            )
        )

        if existing:
            raise ValueError(
                "Bác sĩ đã tồn tại"
            )

        doctor = Doctor(
            user_id=data.user_id,
            specialty=data.specialty,
            room_number=data.room_number,
            years_of_experience=data.years_of_experience
        )

        return DoctorRepository.create(
            db,
            doctor
        )

    @staticmethod
    def get_all_doctors(
        db: Session
    ):
        """
        Lấy danh sách bác sĩ.
        """

        return DoctorRepository.get_all(
            db
        )

    @staticmethod
    def get_doctor(
        db: Session,
        doctor_id: int
    ):
        """
        Lấy thông tin bác sĩ.
        """

        doctor = (
            DoctorRepository.get_by_id(
                db,
                doctor_id
            )
        )

        if not doctor:
            raise ValueError(
                "Không tìm thấy bác sĩ"
            )

        return doctor

    @staticmethod
    def update_doctor(
        db: Session,
        doctor_id: int,
        data: DoctorUpdate
    ):
        """
        Cập nhật bác sĩ.
        """

        doctor = (
            DoctorRepository.get_by_id(
                db,
                doctor_id
            )
        )

        if not doctor:
            raise ValueError(
                "Không tìm thấy bác sĩ"
            )

        if data.specialty is not None:
            doctor.specialty = data.specialty

        if data.room_number is not None:
            doctor.room_number = data.room_number

        if (
            data.years_of_experience
            is not None
        ):
            doctor.years_of_experience = (
                data.years_of_experience
            )

        return DoctorRepository.update(
            db,
            doctor
        )

    @staticmethod
    def delete_doctor(
        db: Session,
        doctor_id: int
    ):
        """
        Xóa bác sĩ.
        """

        doctor = (
            DoctorRepository.get_by_id(
                db,
                doctor_id
            )
        )

        if not doctor:
            raise ValueError(
                "Không tìm thấy bác sĩ"
            )

        DoctorRepository.delete(
            db,
            doctor
        )