from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.base import (
    TimestampMixin
)
from app.utils.constants import (
    PaymentStatus
)

class Invoice(
    Base,
    TimestampMixin
):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    appointment_id: Mapped[int] = mapped_column(
        ForeignKey(
            "appointments.id"
        ),
        unique=True
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.UNPAID
    )

    appointment = relationship(
        "Appointment",
        back_populates="invoice"
    )