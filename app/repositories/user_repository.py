"""
user_repository.py

Chịu trách nhiệm thao tác dữ liệu bảng User.
"""

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository xử lý dữ liệu User.
    """

    @staticmethod
    def create(
        db: Session,
        user: User
    ) -> User:
        """
        Thêm người dùng mới.
        """

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ) -> User | None:
        """
        Tìm user theo ID.
        """

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ) -> User | None:
        """
        Tìm user theo email.
        """

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session
    ) -> list[User]:
        """
        Lấy toàn bộ người dùng.
        """

        return (
            db.query(User)
            .order_by(User.id.desc())
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        user: User
    ):
        """
        Xóa người dùng.
        """

        db.delete(user)

        db.commit()