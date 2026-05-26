"""
auth_service.py

Xử lý nghiệp vụ xác thực người dùng.

Bao gồm:

- Đăng ký tài khoản
- Đăng nhập hệ thống
- Sinh Access Token
- Sinh Refresh Token
"""

from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.user import UserCreate

from app.repositories.user_repository import (
    UserRepository
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)


class AuthService:
    """
    Service xử lý xác thực người dùng.
    """

    @staticmethod
    def register(
        db: Session,
        user_data: UserCreate
    ) -> User:
        """
        Đăng ký tài khoản mới.

        Quy trình:

        1. Kiểm tra email đã tồn tại hay chưa
        2. Mã hóa mật khẩu
        3. Tạo tài khoản mới
        4. Lưu xuống cơ sở dữ liệu

        Args:
            db:
                Session kết nối database

            user_data:
                Dữ liệu đăng ký từ người dùng

        Returns:
            User vừa được tạo
        """

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise ValueError(
                "Email đã tồn tại trong hệ thống"
            )

        new_user = User(
            fullname=user_data.fullname,
            email=user_data.email,
            phone=user_data.phone,
            role=user_data.role,
            hashed_password=hash_password(
                user_data.password
            )
        )

        return UserRepository.create(
            db,
            new_user
        )

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ) -> dict:
        """
        Đăng nhập hệ thống.

        Quy trình:

        1. Kiểm tra email tồn tại
        2. Kiểm tra mật khẩu
        3. Sinh Access Token
        4. Sinh Refresh Token
        5. Trả thông tin đăng nhập

        Args:
            db:
                Session kết nối database

            email:
                Email đăng nhập

            password:
                Mật khẩu đăng nhập

        Returns:
            Thông tin đăng nhập gồm:
            - access_token
            - refresh_token
            - token_type
            - fullname
            - role
        """

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise ValueError(
                "Email không tồn tại"
            )

        if not verify_password(
            password,
            user.hashed_password
        ):
            raise ValueError(
                "Mật khẩu không chính xác"
            )

        # Sinh Access Token
        access_token = create_access_token(
            {
                "sub": user.email,
                "role": user.role
            }
        )

        # Sinh Refresh Token
        refresh_token = create_refresh_token(
            {
                "sub": user.email
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "fullname": user.fullname,
            "role": user.role
        }