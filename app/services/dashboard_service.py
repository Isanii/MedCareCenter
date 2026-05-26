"""
dashboard_service.py

Xử lý nghiệp vụ Dashboard.
"""

from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import (
    DashboardRepository
)


class DashboardService:

    @staticmethod
    def get_dashboard(
        db: Session
    ):
        """
        Lấy dữ liệu Dashboard.
        """

        return (
            DashboardRepository
            .get_statistics(
                db
            )
        )