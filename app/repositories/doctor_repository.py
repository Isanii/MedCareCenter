"""
doctor_repository.py

Thao tác dữ liệu bảng Doctor.
"""
from sqlalchemy import or_
from app.models.user import User
from sqlalchemy.orm import (
    Session,
    joinedload
)

from app.models.doctor import Doctor


class DoctorRepository:
    """
    Repository quản lý dữ liệu bác sĩ.
    """

    @staticmethod
    def create(
        db: Session,
        doctor: Doctor
    ) -> Doctor:
        """
        Tạo bác sĩ mới.
        """

        db.add(doctor)

        db.commit()

        db.refresh(doctor)

        return doctor

    @staticmethod
    def get_by_id(
        db: Session,
        doctor_id: int
    ) -> Doctor | None:
        """
        Tìm bác sĩ theo ID.
        """

        return (
            db.query(Doctor)
            .options(
                joinedload(
                    Doctor.user
                )
            )
            .filter(
                Doctor.id == doctor_id
            )
            .first()
        )

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Doctor)
            .filter(
                Doctor.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20
    ) -> list[Doctor]:
        """
        Lấy danh sách bác sĩ có phân trang.
        """

        return (
            db.query(Doctor)
            .options(
                joinedload(
                    Doctor.user
                )
            )
            .order_by(
                Doctor.id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        doctor: Doctor
    ) -> Doctor:
        """
        Cập nhật thông tin bác sĩ.
        """

        db.commit()

        db.refresh(doctor)

        return doctor

    @staticmethod
    def delete(
        db: Session,
        doctor: Doctor
    ):
        """
        Xóa bác sĩ.
        """

        db.delete(doctor)

        db.commit()

    @staticmethod
    def search_by_specialty(
        db: Session,
        specialty: str
    ) -> list[Doctor]:
        """
        Tìm bác sĩ theo chuyên khoa.
        """

        return (
            db.query(Doctor)
            .options(
                joinedload(
                    Doctor.user
                )
            )
            .filter(
                Doctor.specialty.contains(
                    specialty
                )
            )
            .order_by(
                Doctor.id
            )
            .all()
        )

    @staticmethod
    def search(
        db: Session,
        keyword: str | None = None,
        min_exp: int | None = None
    ):
        """
        Tìm kiếm bác sĩ theo:
        - Họ tên
        - Email
        - Chuyên khoa
        """

        query = (
            db.query(Doctor)
            .join(User)
            .options(
                joinedload(
                    Doctor.user
                )
            )
        )

        if keyword:

            query = query.filter(
                or_(
                    User.fullname.contains(
                        keyword
                    ),
                    User.email.contains(
                        keyword
                    ),
                    Doctor.specialty.contains(
                        keyword
                    )
                )
            )

        if min_exp is not None:

            query = query.filter(
                Doctor.years_of_experience
                >= min_exp
            )

        return (
            query
            .order_by(
                Doctor.id
            )
            .all()
        )