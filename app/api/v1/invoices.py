from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceUpdateStatus
)

from app.services.invoice_service import (
    InvoiceService
)

ReceptionOrAdmin = Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.RECEPTIONIST
    )
)

router = APIRouter(
    prefix="/api/v1/invoices",
    tags=["Invoices"]
)


#Tạo hóa đơn
@router.post(
    "/",
    response_model=InvoiceResponse
)
def create_invoice(
    data: InvoiceCreate,
    db: Session = Depends(get_db)
):
    try:

        return (
            InvoiceService
            .create_invoice(
                db,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

#Danh sách hóa đơn
@router.get(
    "/",
    response_model=list[
        InvoiceResponse
    ]
)
def get_all(
    db: Session = Depends(get_db)
):
    return (
        InvoiceService.get_all(
            db
        )
    )

#Chi tiết hóa đơn
@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse
)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    try:

        return (
            InvoiceService.get_invoice(
                db,
                invoice_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

#Thanh toán
@router.patch(
    "/{invoice_id}/status",
    response_model=InvoiceResponse
)
def update_status(
    _ = ReceptionOrAdmin,
    invoice_id: int,
    data: InvoiceUpdateStatus,
    db: Session = Depends(get_db)
):
    try:

        return (
            InvoiceService.update_status(
                db,
                invoice_id,
                data.payment_status
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
