"""
dashboard.py

API Dashboard.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.dashboard import (
    DashboardResponse
)

from app.services.dashboard_service import (
    DashboardService
)

from app.dependencies.auth import (
    get_current_user
)

from app.dependencies.roles import (
    AdminOnly,
    DoctorOnly,
    PatientOnly
)

from app.models.user import User

from app.services.appointment_service import (
    AppointmentService
)

from app.services.medical_record_service import (
    MedicalRecordService
)

from app.services.invoice_service import (
    InvoiceService
)

from app.repositories.doctor_repository import (
    DoctorRepository
)

from app.repositories.appointment_repository import (
    AppointmentRepository
)

from app.repositories.medical_record_repository import (
    MedicalRecordRepository
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

@router.get(
    "/patient",
    dependencies=[
        Depends(PatientOnly)
    ]
)
def patient_dashboard(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    appointments = (
        AppointmentService
        .get_my_appointments(
            db,
            current_user
        )
    )

    records = (
        MedicalRecordService
        .get_my_records(
            db,
            current_user
        )
    )

    invoices = (
        InvoiceService
        .get_my_invoices(
            db,
            current_user
        )
    )

    paid_count = len([
        invoice
        for invoice in invoices
        if str(
            invoice.payment_status
        ).lower().endswith(
            "paid"
        )
    ])

    return {
        "appointment_count":
            len(
                appointments
            ),

        "record_count":
            len(
                records
            ),

        "invoice_count":
            len(
                invoices
            ),

        "paid_invoice_count":
            paid_count
    }

@router.get(
    "/doctor",
    dependencies=[
        Depends(DoctorOnly)
    ]
)
def doctor_dashboard(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    doctor = (
        DoctorRepository
        .get_by_user_id(
            db,
            current_user.id
        )
    )

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy bác sĩ"
        )

    appointments = (
        AppointmentRepository
        .get_by_doctor_id(
            db,
            doctor.id
        )
    )

    records = (
        MedicalRecordRepository
        .get_by_doctor_id(
            db,
            doctor.id
        )
    )

    return {

        "appointment_count":
            len(
                appointments
            ),

        "pending_count":
            len([
                x
                for x in appointments
                if x.status
                ==
                "pending"
            ]),

        "completed_count":
            len([
                x
                for x in appointments
                if x.status
                ==
                "completed"
            ]),

        "record_count":
            len(
                records
            )
    }