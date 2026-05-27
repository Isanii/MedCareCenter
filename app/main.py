from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import (router as auth_router)
from app.api.v1.doctors import (router as doctor_router)
from app.api.v1.patients import (router as patient_router)
from app.api.v1.appointments import (router as appointment_router)
from app.api.v1.medical_records import (router as medical_record_router)
from app.api.v1.invoices import (router as invoice_router)
from app.api.v1.dashboard import (router as dashboard_router)
from app.core.middleware import (logging_middleware)
from app.core.exceptions import (value_error_handler)
from app.api.v1 import user
from app.core.database import (
    Base,
    engine
)
import app.models
# Tạo bảng nếu chưa tồn tại
Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="MedCare API",
    description="""
    Hệ thống quản lý phòng khám MedCare.

    Chức năng:

    - Xác thực JWT
    - Quản lý bác sĩ
    - Quản lý bệnh nhân
    - Quản lý lịch hẹn
    - Quản lý hồ sơ bệnh án
    - Quản lý hóa đơn
    - Dashboard thống kê
    """,
    version="2.0.0",
    contact={
        "name": "MedCare Team"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(
    logging_middleware
)

app.add_exception_handler(
    ValueError,
    value_error_handler
)

# Đăng ký router
app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(medical_record_router)
app.include_router(invoice_router)
app.include_router(dashboard_router)
app.include_router(user.router)
@app.get("/")
def root():
    return {
        "message": "MEDCARE CENTER"
    }

@app.get(
    "/health",
    tags=["System"]
)
def health_check():
    """
    Kiểm tra trạng thái hệ thống.
    """

    return {
        "status": "healthy",
        "service": "MedCare API",
        "version": "2.0"
    }