"""
doctor_service.py

Xử lý nghiệp vụ bác sĩ.
"""

from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.models.user import User

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorCreateWithUser
)

from app.repositories.doctor_repository import (
    DoctorRepository
)

from app.repositories.user_repository import (
    UserRepository
)

from app.core.security import (
    hash_password
)

from app.utils.constants import (
    UserRole
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
        Tạo hồ sơ bác sĩ từ user có sẵn.
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
    def create_doctor_with_user(
        db: Session,
        data: DoctorCreateWithUser
    ):
        """
        Tạo User và Doctor cùng lúc.
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
            role=UserRole.DOCTOR,
            hashed_password=hash_password(
                data.password
            )
        )

        db.add(user)

        # Lấy user.id trước commit
        db.flush()

        doctor = Doctor(
            user_id=user.id,
            specialty=data.specialty,
            room_number=data.room_number,
            years_of_experience=data.years_of_experience
        )

        db.add(doctor)

        db.commit()

        db.refresh(doctor)

        return doctor

    @staticmethod
    def get_all_doctors(
        db: Session,
        skip: int = 0,
        limit: int = 20
    ):
        """
        Danh sách bác sĩ.
        """

        return (
            DoctorRepository.get_all(
                db,
                skip,
                limit
            )
        )

    @staticmethod
    def get_doctor(
        db: Session,
        doctor_id: int
    ):
        """
        Chi tiết bác sĩ.
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

        if data.years_of_experience is not None:
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

    @staticmethod
    def search_doctors(
        db: Session,
        specialty: str
    ):
        """
        Tìm bác sĩ theo chuyên khoa.
        """

        return (
            DoctorRepository.search_by_specialty(
                db,
                specialty
            )
        )

    @staticmethod
    def search(
        db: Session,
        keyword: str | None = None,
        min_exp: int | None = None
    ):
        return (
            DoctorRepository.search(
                db,
                keyword,
                min_exp
            )
        )