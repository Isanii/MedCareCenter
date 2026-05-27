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
    LoginRequest,
    LoginResponse
)

from app.services.auth_service import (
    AuthService
)

from app.core.security import (
    hash_password
)

from app.models.user import User

from app.services.otp_service import (
    OTPService
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

from fastapi_mail import (
    FastMail,
    MessageSchema
)

from app.core.mail import (
    conf
)

from app.services.otp_service import (
    OTPService
)

#API Đăng Ký
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Đăng ký tài khoản",
    description="""
    Tạo tài khoản người dùng mới.

    Email phải là duy nhất trong hệ thống.
    """
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Đăng ký tài khoản mới.
    """

    return AuthService.register(
        db,
        user_data
    )

#API Đăng Nhập
@router.post(
    "/login",
    summary="Đăng nhập hệ thống",
    description="""
    Đăng nhập bằng email và mật khẩu.

    Trả về:

    - access_token
    - refresh_token
    """
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Đăng nhập hệ thống.
    """

    return AuthService.login(
        db,
        login_data.email,
        login_data.password
    )

#API Lấy User Hiện Tại
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Thông tin người dùng hiện tại"
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


@router.post(
    "/forgot-password"
)
async def forgot_password(
    email: str
):

    otp = OTPService.generate(
        email
    )

    message = MessageSchema(

        subject=
            "MedCare OTP",

        recipients=[
            email
        ],

        body=
            f"Ma OTP cua ban la: {otp}",

        subtype="plain"
    )

    fm = FastMail(
        conf
    )

    await fm.send_message(
        message
    )

    return {
        "message":
        "OTP da duoc gui"
    }


@router.post(
    "/verify-otp"
)
def verify_otp(
    email: str,
    otp: str
):

    if not OTPService.verify(
        email,
        otp
    ):

        raise HTTPException(
            status_code=400,
            detail=
            "OTP khong dung"
        )

    return {
        "message":
        "OTP hop le"
    }


@router.post(
    "/reset-password"
)
def reset_password(
    email: str,
    otp: str,
    new_password: str,
    db: Session = Depends(
        get_db
    )
):

    if not OTPService.verify(
        email,
        otp
    ):

        raise HTTPException(
            status_code=400,
            detail=
            "OTP không hợp lệ"
        )

    user = (
        db.query(User)
        .filter(
            User.email
            == email
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail=
            "Không tìm thấy tài khoản"
        )

    user.hashed_password = (
        hash_password(
            new_password
        )
    )

    db.commit()

    return {
        "message":
        "Đổi mật khẩu thành công"
    }