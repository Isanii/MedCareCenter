"""
dashboard_repository.py

Repository thống kê dữ liệu Dashboard.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User

from app.models.doctor import Doctor

from app.models.patient import Patient

from app.models.appointment import Appointment

from app.models.medical_record import (
    MedicalRecord
)

from app.models.invoice import Invoice

from app.utils.constants import (
    PaymentStatus
)


class DashboardRepository:

    @staticmethod
    def get_statistics(
        db: Session
    ):
        """
        Thống kê tổng quan.
        """

        total_users = (
            db.query(User)
            .count()
        )

        total_doctors = (
            db.query(Doctor)
            .count()
        )

        total_patients = (
            db.query(Patient)
            .count()
        )

        total_appointments = (
            db.query(Appointment)
            .count()
        )

        total_medical_records = (
            db.query(MedicalRecord)
            .count()
        )

        total_invoices = (
            db.query(Invoice)
            .count()
        )

        paid_invoices = (
            db.query(Invoice)
            .filter(
                Invoice.payment_status
                == PaymentStatus.PAID
            )
            .count()
        )

        unpaid_invoices = (
            db.query(Invoice)
            .filter(
                Invoice.payment_status
                == PaymentStatus.UNPAID
            )
            .count()
        )

        revenue = (
            db.query(
                func.sum(
                    Invoice.amount
                )
            )
            .filter(
                Invoice.payment_status
                == PaymentStatus.PAID
            )
            .scalar()
        )

        return {
            "total_users": total_users,
            "total_doctors": total_doctors,
            "total_patients": total_patients,
            "total_appointments": total_appointments,
            "total_medical_records":
                total_medical_records,
            "total_invoices":
                total_invoices,
            "paid_invoices":
                paid_invoices,
            "unpaid_invoices":
                unpaid_invoices,
            "total_revenue":
                revenue or 0
        }