"""
doctor_repository.py

Thao tác dữ liệu bảng Doctor.
"""

from sqlalchemy.orm import Session

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
            .filter(
                Doctor.id == doctor_id
            )
            .first()
        )

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int
    ) -> Doctor | None:
        """
        Tìm bác sĩ theo user_id.
        """

        return (
            db.query(Doctor)
            .filter(
                Doctor.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session
    ) -> list[Doctor]:
        """
        Lấy danh sách bác sĩ.
        """

        return (
            db.query(Doctor)
            .order_by(
                Doctor.id.desc()
            )
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