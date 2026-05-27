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

AdminOnly = require_roles(
    UserRole.ADMIN
)

DoctorOnly = require_roles(
    UserRole.DOCTOR
)

PatientOnly = require_roles(
    UserRole.PATIENT
)

ReceptionistOnly = require_roles(
    UserRole.RECEPTIONIST
)

ReceptionOrAdmin = require_roles(
    UserRole.ADMIN,
    UserRole.RECEPTIONIST
)

DoctorOrAdmin = require_roles(
    UserRole.ADMIN,
    UserRole.DOCTOR
)