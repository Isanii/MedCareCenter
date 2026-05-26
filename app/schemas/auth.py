"""
auth.py

Schema phục vụ xác thực người dùng.

Bao gồm:

- Đăng nhập
- JWT Token
"""

from pydantic import BaseModel
from pydantic import EmailStr


class LoginRequest(BaseModel):
    """
    Dữ liệu đăng nhập.
    """

    email: EmailStr

    password: str


class TokenResponse(BaseModel):
    """
    Dữ liệu trả về sau khi đăng nhập thành công.
    """

    access_token: str

    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Dữ liệu lưu trong JWT.
    """

    sub: str

    role: str

class LoginResponse(BaseModel):
    """
    Dữ liệu trả về khi đăng nhập.
    """

    access_token: str

    refresh_token: str

    token_type: str

    fullname: str

    role: str