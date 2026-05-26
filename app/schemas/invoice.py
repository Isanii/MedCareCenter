from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from app.utils.constants import (PaymentStatus)


class InvoiceCreate(
    BaseModel
):
    """
    Tạo hóa đơn.
    """

    appointment_id: int

    amount: float


class InvoiceUpdateStatus(
    BaseModel
):
    """
    Cập nhật trạng thái thanh toán.
    """

    payment_status: PaymentStatus

class InvoiceResponse(
    BaseModel
):
    """
    Thông tin hóa đơn.
    """

    id: int

    appointment_id: int

    amount: float

    payment_status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )