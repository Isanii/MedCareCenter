from datetime import datetime

from pydantic import BaseModel


class MessageCreate(
    BaseModel
):

    receiver_id: int

    content: str


class MessageResponse(
    BaseModel
):

    id: int

    sender_id: int

    receiver_id: int

    content: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }