"""
invoice_repository.py

Repository quản lý hóa đơn.
"""

from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.models.appointment import (
    Appointment
)

class InvoiceRepository:

    @staticmethod
    def create(
        db: Session,
        invoice: Invoice
    ) -> Invoice:

        db.add(invoice)

        db.commit()

        db.refresh(invoice)

        return invoice

    @staticmethod
    def get_by_id(
        db: Session,
        invoice_id: int
    ) -> Invoice | None:

        return (
            db.query(Invoice)
            .filter(
                Invoice.id == invoice_id
            )
            .first()
        )

    @staticmethod
    def get_by_appointment(
        db: Session,
        appointment_id: int
    ) -> Invoice | None:

        return (
            db.query(Invoice)
            .filter(
                Invoice.appointment_id
                == appointment_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20
    ):
        """
        Lấy danh sách hóa đơn có phân trang.
        """

        return (
            db.query(Invoice)
            .order_by(
                Invoice.id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        invoice: Invoice
    ) -> Invoice:

        db.commit()

        db.refresh(invoice)

        return invoice

    @staticmethod
    def delete(
        db: Session,
        invoice: Invoice
    ):
        db.delete(invoice)

        db.commit()

    @staticmethod
    def get_by_patient_id(
        db: Session,
        patient_id: int
    ):
        """
        Lấy hóa đơn theo bệnh nhân.
        """

        return (
            db.query(Invoice)
            .join(
                Appointment,
                Invoice.appointment_id
                ==
                Appointment.id
            )
            .filter(
                Appointment.patient_id
                ==
                patient_id
            )
            .all()
        )