"""
permission.py

Kiểm tra quyền truy cập API.
"""

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.auth import (
    get_current_user
)

from app.utils.constants import (
    UserRole
)


def require_roles(
    *allowed_roles: UserRole
):
    """
    Dependency kiểm tra role.
    """

    def checker(
        current_user=Depends(
            get_current_user
        )
    ):
        if (
            current_user.role
            not in allowed_roles
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập"
            )

        return current_user

    return checker