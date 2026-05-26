"""
dashboard.py

Schema thống kê tổng quan hệ thống.
"""

from pydantic import BaseModel


class DashboardResponse(
    BaseModel
):
    """
    Dữ liệu Dashboard.
    """

    total_users: int

    total_doctors: int

    total_patients: int

    total_appointments: int

    total_medical_records: int

    total_invoices: int

    paid_invoices: int

    unpaid_invoices: int

    total_revenue: float