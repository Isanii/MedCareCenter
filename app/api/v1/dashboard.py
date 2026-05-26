"""
dashboard.py

API Dashboard.
"""

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.dashboard import (
    DashboardResponse
)

from app.services.dashboard_service import (
    DashboardService
)

#Admin mới xem được dashboard
from app.dependencies.roles import (
    AdminOnly
)

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

#API Thống kê
@router.get(
    "/",
    response_model=DashboardResponse
)
def get_dashboard(
    db: Session = Depends(get_db)
):
    """
    Thống kê tổng quan hệ thống.
    """

    return (
        DashboardService
        .get_dashboard(
            db
        )
    )




@router.get(
    "/",
    response_model=DashboardResponse
)
def get_dashboard(
    _ = AdminOnly,
    db: Session = Depends(get_db)
):
    """
    Dashboard chỉ dành cho Admin.
    """

    return (
        DashboardService
        .get_dashboard(db)
    )