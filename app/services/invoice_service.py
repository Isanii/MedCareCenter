"""
invoice_service.py

Xử lý nghiệp vụ hóa đơn.
"""

from sqlalchemy.orm import Session

from app.models.invoice import Invoice

from app.repositories.invoice_repository import (
    InvoiceRepository
)

from app.repositories.appointment_repository import (
    AppointmentRepository
)

from app.schemas.invoice import (
    InvoiceCreate
)
from app.utils.constants import (
    PaymentStatus
)

from app.models.user import User

from app.repositories.patient_repository import (
    PatientRepository
)

class InvoiceService:

    @staticmethod
    def create_invoice(
        db: Session,
        data: InvoiceCreate
    ):
        """
        Tạo hóa đơn.
        """

        appointment = (
            AppointmentRepository
            .get_by_id(
                db,
                data.appointment_id
            )
        )

        if not appointment:
            raise ValueError(
                "Không tìm thấy lịch hẹn"
            )

        existing = (
            InvoiceRepository
            .get_by_appointment(
                db,
                data.appointment_id
            )
        )

        if existing:
            raise ValueError(
                "Hóa đơn đã tồn tại"
            )
        if data.amount <= 0:
            raise ValueError(
                "Số tiền phải lớn hơn 0"
            )

        invoice = Invoice(
            appointment_id=data.appointment_id,
            amount=data.amount,
            payment_status=
                PaymentStatus.UNPAID
        )
        return InvoiceRepository.create(
            db,
            invoice
        )

    @staticmethod
    def get_invoice(
        db: Session,
        invoice_id: int
    ):
        invoice = (
            InvoiceRepository.get_by_id(
                db,
                invoice_id
            )
        )

        if not invoice:
            raise ValueError(
                "Không tìm thấy hóa đơn"
            )

        return invoice

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20
    ):
        """
        Lấy danh sách hóa đơn.
        """

        return (
            InvoiceRepository.get_all(
                db,
                skip,
                limit
            )
        )

    @staticmethod
    def update_status(
        db: Session,
        invoice_id: int,
        status: str
    ):
        invoice = (
            InvoiceRepository.get_by_id(
                db,
                invoice_id
            )
        )

        if not invoice:
            raise ValueError(
                "Không tìm thấy hóa đơn"
            )

        invoice.payment_status = status

        return InvoiceRepository.update(
            db,
            invoice
        )
    @staticmethod
    def delete_invoice(
        db: Session,
        invoice_id: int
    ):
        invoice = (
            InvoiceRepository
            .get_by_id(
                db,
                invoice_id
            )
        )

        if not invoice:
            raise ValueError(
                "Không tìm thấy hóa đơn"
            )

        InvoiceRepository.delete(
            db,
            invoice
        )

    @staticmethod
    def get_my_invoices(
        db: Session,
        current_user: User
    ):
        """
        Hóa đơn của bệnh nhân đang đăng nhập.
        """

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
            InvoiceRepository
            .get_by_patient_id(
                db,
                patient.id
            )
        )