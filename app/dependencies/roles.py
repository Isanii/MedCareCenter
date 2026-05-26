"""
roles.py

Các dependency role dùng lại.
"""

from fastapi import Depends

from app.dependencies.permission import (
    require_roles
)

from app.utils.constants import (
    UserRole
)


AdminOnly = Depends(
    require_roles(
        UserRole.ADMIN
    )
)

DoctorOnly = Depends(
    require_roles(
        UserRole.DOCTOR
    )
)

ReceptionistOnly = Depends(
    require_roles(
        UserRole.RECEPTIONIST
    )
)

PatientOnly = Depends(
    require_roles(
        UserRole.PATIENT
    )
)