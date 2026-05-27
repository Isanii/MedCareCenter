from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.user import User

from app.repositories.user_repository import (
    UserRepository
)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.put(
    "/{user_id}/status"
)
def update_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db)
):

    user = UserRepository.get_by_id(
        db,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài khoản"
        )

    user.is_active = is_active

    db.commit()

    db.refresh(user)

    return {
        "message":
        "Cập nhật trạng thái thành công"
    }