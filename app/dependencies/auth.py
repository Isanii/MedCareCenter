"""
auth.py

Dependency xác thực và phân quyền.
"""

from jose import jwt
from jose import JWTError

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status


from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

from app.repositories.user_repository import (
    UserRepository
)
from fastapi.security import HTTPBearer

security = HTTPBearer()


from fastapi.security import HTTPAuthorizationCredentials


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    """
    Giải mã JWT và lấy user hiện tại.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Phiên đăng nhập không hợp lệ"
    )

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        UserRepository.get_by_email(
            db,
            email
        )
    )

    if user is None:
        raise credentials_exception

    return user


def require_roles(
    allowed_roles: list
):
    """
    Dependency kiểm tra quyền.
    """

    def role_checker(
        current_user=Depends(
            get_current_user
        )
    ):

        if (
            current_user.role
            not in allowed_roles
        ):
            raise HTTPException(
                status_code=403,
                detail="Không đủ quyền truy cập"
            )

        return current_user

    return role_checker