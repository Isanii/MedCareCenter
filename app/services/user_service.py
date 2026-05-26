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