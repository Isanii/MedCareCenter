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


@router.get(
    "/",
    response_model=DashboardResponse,
    dependencies=[Depends(AdminOnly)]
)
def get_dashboard(
    db: Session = Depends(get_db)
):
    return DashboardService.get_dashboard(
        db
    )