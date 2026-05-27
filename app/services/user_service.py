"""
user_service.py

Nghiệp vụ liên quan tới người dùng.
"""

from sqlalchemy.orm import Session

from app.repositories.user_repository import (
    UserRepository
)


class UserService:

    @staticmethod
    def get_user(
        db: Session,
        user_id: int
    ):
        """
        Lấy người dùng theo ID.
        """

        return UserRepository.get_by_id(
            db,
            user_id
        )

    @staticmethod
    def get_all_users(
        db: Session
    ):
        """
        Lấy toàn bộ người dùng.
        """

        return UserRepository.get_all(db)

    @staticmethod
    def set_active_status(
        db: Session,
        user_id: int,
        is_active: bool
    ):
        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise ValueError(
                "Không tìm thấy tài khoản"
            )

        user.is_active = is_active

        db.commit()

        db.refresh(user)

        return user