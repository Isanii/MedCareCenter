from sqlalchemy import ForeignKey
from sqlalchemy import UnicodeText

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.core.database import Base
from app.models.base import TimestampMixin


class Message(
    Base,
    TimestampMixin
):

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    content: Mapped[str] = mapped_column(
        UnicodeText
    )