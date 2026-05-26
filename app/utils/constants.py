from enum import Enum

class UserRole(str, Enum):
    """
    Danh sách vai trò của hệ thống.
    """

    ADMIN = "admin"

    DOCTOR = "doctor"

    RECEPTIONIST = "receptionist"

    PATIENT = "patient"

class AppointmentStatus(str, Enum):
    PENDING = "pending"

    CONFIRMED = "confirmed"

    CHECKED_IN = "checked_in"

    IN_PROGRESS = "in_progress"

    COMPLETED = "completed"

    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    UNPAID = "unpaid"

    PAID = "paid"