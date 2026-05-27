from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.dependencies.auth import (
    get_current_user
)

from app.models.message import (
    Message
)

from app.schemas.message import (
    MessageCreate
)

router = APIRouter(
    prefix="/api/v1/messages",
    tags=["Messages"]
)


@router.post("")
def send_message(
    data: MessageCreate,
    db: Session = Depends(
        get_db
    ),
    current_user = Depends(
        get_current_user
    )
):

    message = Message(

        sender_id=
            current_user.id,

        receiver_id=
            data.receiver_id,

        content=
            data.content
    )

    db.add(
        message
    )

    db.commit()

    return {
        "message":
        "Đã gửi"
    }


@router.get(
    "/conversation/{user_id}"
)
def get_conversation(
    user_id: int,
    db: Session = Depends(
        get_db
    ),
    current_user = Depends(
        get_current_user
    )
):

    messages = (

        db.query(Message)

        .filter(

            (
                (Message.sender_id == current_user.id)
                &
                (Message.receiver_id == user_id)
            )

            |

            (
                (Message.sender_id == user_id)
                &
                (Message.receiver_id == current_user.id)
            )

        )

        .order_by(
            Message.created_at
        )

        .all()
    )

    return messages