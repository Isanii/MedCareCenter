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


from app.dependencies.auth import (
    get_current_user
)

from app.models.user import (
    User
)

from app.dependencies.roles import (
    ReceptionOrAdmin,
    PatientOnly
)

router = APIRouter(
    prefix="/api/v1/invoices",
    tags=["Invoices"]
)


#Tạo hóa đơn
@router.post(
    "/",
    response_model=InvoiceResponse,
    status_code=201,
    summary="Tạo hóa đơn",
    description="""
    Tạo hóa đơn cho một lịch hẹn khám bệnh.
    """
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
    ],
    dependencies=[
        Depends(
            ReceptionOrAdmin
        )
    ]
)
def get_all(
    db: Session = Depends(
        get_db
    )
):
    return (
        InvoiceService
        .get_all(
            db
        )
    )

@router.get(
    "/my",
    response_model=list[
        InvoiceResponse
    ],
    dependencies=[
        Depends(PatientOnly)
    ]
)
def my_invoices(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    try:

        return (
            InvoiceService
            .get_my_invoices(
                db,
                current_user
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
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
    response_model=InvoiceResponse,
    dependencies=[Depends(ReceptionOrAdmin)],
    summary="Thanh toán hóa đơn",
    description="""
    Cập nhật trạng thái thanh toán.

    Chỉ Receptionist hoặc Admin được phép.
    """
)
def update_status(
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


@router.delete(
    "/{invoice_id}",
    dependencies=[
        Depends(ReceptionOrAdmin)
    ]
)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    try:

        InvoiceService.delete_invoice(
            db,
            invoice_id
        )

        return {
            "message":
            "Xóa hóa đơn thành công"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

