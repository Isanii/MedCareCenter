"""
patient_repository.py

Thao tác dữ liệu bệnh nhân.
"""
from sqlalchemy.orm import (
    Session,
    joinedload
)
from app.models.patient import Patient
from app.models.user import User

class PatientRepository:

    @staticmethod
    def create(
        db: Session,
        patient: Patient
    ) -> Patient:

        db.add(patient)

        db.commit()

        db.refresh(patient)

        return patient

    @staticmethod
    def get_by_id(
        db: Session,
        patient_id: int
    ) -> Patient | None:

        return (
            db.query(Patient)
            .options(
                joinedload(
                    Patient.user
                )
            )
            .filter(
                Patient.id == patient_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20
    ) -> list[Patient]:
        """
        Lấy danh sách bệnh nhân có phân trang.
        """

        return (
            db.query(Patient)
            .options(
                joinedload(
                    Patient.user
                )
            )
            .order_by(
                Patient.id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

#Tìm bệnh nhân theo user id, cập nhật bệnh nhân, xóa bệnh nhân
    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int
    ) -> Patient | None:
        """
        Tìm bệnh nhân theo user_id.
        """

        return (
            db.query(Patient)
            .filter(
                Patient.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        patient: Patient
    ) -> Patient:
        """
        Cập nhật bệnh nhân.
        """

        db.commit()

        db.refresh(patient)

        return patient

    @staticmethod
    def delete(
        db: Session,
        patient: Patient
    ):
        """
        Xóa bệnh nhân.
        """

        db.delete(patient)

        db.commit()


    @staticmethod
    def search(
        db: Session,
        keyword: str
    ):
        """
        Tìm kiếm bệnh nhân theo:
        - Họ tên
        - Số điện thoại
        - Địa chỉ
        """

        return (
            db.query(Patient)
            .join(User)
            .options(
                joinedload(
                    Patient.user
                )
            )
            .filter(
                (User.fullname.contains(keyword))
                |
                (User.phone.contains(keyword))
                |
                (Patient.address.contains(keyword))
            )
            .order_by(
                Patient.id
            )
            .all()
        )

    