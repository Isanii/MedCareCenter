"""
auth.py

API xác thực người dùng.

Bao gồm:

- Đăng ký
- Đăng nhập
- Lấy thông tin tài khoản hiện tại
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dependencies.auth import (
    get_current_user
)

from app.schemas.user import (
    UserCreate,
    UserResponse
)

from app.schemas.auth import (
    LoginRequest
)

from app.services.auth_service import (
    AuthService
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

#API Đăng Ký
@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Đăng ký tài khoản mới.
    """

    try:

        return AuthService.register(
            db,
            user_data
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

#API Đăng Nhập
@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Đăng nhập hệ thống.
    """

    try:

        return AuthService.login(
            db,
            login_data.email,
            login_data.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

#API Lấy User Hiện Tại
@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user=Depends(
        get_current_user
    )
):
    """
    Lấy thông tin người dùng hiện tại.
    """

    return current_user