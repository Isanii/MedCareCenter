"""
Import toàn bộ model của hệ thống.

Alembic sẽ đọc file này để tự động
phát hiện các bảng cần sinh migration.
"""

from .user import User
from .doctor import Doctor
from .patient import Patient
from .appointment import Appointment
from .medical_record import MedicalRecord
from .invoice import Invoice
from .message import Message
__all__ = [
    "User",
    "Doctor",
    "Patient",
    "Appointment",
    "MedicalRecord",
    "Invoice"
]