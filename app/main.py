from fastapi import FastAPI

from app.api.v1.auth import (router as auth_router)
from app.api.v1.doctors import (router as doctor_router)
from app.api.v1.patients import (router as patient_router)
from app.api.v1.appointments import (router as appointment_router)
from app.api.v1.medical_records import (router as medical_record_router)
from app.api.v1.invoices import (router as invoice_router)
from app.api.v1.dashboard import (router as dashboard_router)
from app.core.middleware import (logging_middleware)

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
    version="2.0.0"
)

app.middleware("http")(
    logging_middleware
)

# Đăng ký router
app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(medical_record_router)
app.include_router(invoice_router)
app.include_router(dashboard_router)

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