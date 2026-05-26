"""
user.py

Schema quản lý tài khoản người dùng.
"""

from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    """
    Thông tin cơ bản của người dùng.
    """

    fullname: str

    email: EmailStr

    phone: str | None = None


class UserCreate(UserBase):
    """
    Dữ liệu đăng ký tài khoản.
    """

    password: str

    role: str = "patient"


class UserUpdate(BaseModel):
    """
    Dữ liệu cập nhật tài khoản.
    """

    fullname: str | None = None

    phone: str | None = None


class UserResponse(UserBase):
    """
    Dữ liệu trả về từ API.
    """

    id: int

    role: str

    is_active: bool

    created_at: datetime

    model_config = {
        "from_attributes": True
    }