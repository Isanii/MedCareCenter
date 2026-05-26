"""
invoice_repository.py

Repository quản lý hóa đơn.
"""

from sqlalchemy.orm import Session

from app.models.invoice import Invoice


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
        db: Session
    ) -> list[Invoice]:
        return (
            db.query(Invoice)
            .order_by(
                Invoice.id.desc()
            )
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