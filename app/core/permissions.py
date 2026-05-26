"""
permissions.py

Quản lý phân quyền hệ thống.

Vai trò:

- admin
- receptionist
- doctor
- patient
"""

from app.utils.constants import UserRole


class Permission:
    """
    Các nhóm quyền truy cập.
    """

    ADMIN_ONLY = [
        UserRole.ADMIN
    ]

    DOCTOR_ONLY = [
        UserRole.DOCTOR
    ]

    RECEPTIONIST_ONLY = [
        UserRole.RECEPTIONIST
    ]

    PATIENT_ONLY = [
        UserRole.PATIENT
    ]

    STAFF = [
        UserRole.ADMIN,
        UserRole.RECEPTIONIST
    ]

    MEDICAL_STAFF = [
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.RECEPTIONIST
    ]