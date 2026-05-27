"""
patients.py

API quản lý bệnh nhân.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.patient_service import (
    PatientService
)

from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientCreateWithUser
)

from app.dependencies.roles import (
    AdminOnly
)

router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"]
)

#Danh sách bệnh nhân
@router.get(
    "/",
    response_model=list[PatientResponse],
    summary="Danh sách bệnh nhân"
)
def get_patients(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách bệnh nhân.
    """

    return (
        PatientService.get_all_patients(
            db,
            skip,
            limit
        )
    )

@router.get(
    "/search",
    response_model=list[PatientResponse],
    summary="Tìm kiếm bệnh nhân",
    description="""
    Tìm theo:

    - Họ tên
    - Số điện thoại
    - Địa chỉ
    """
)
def search_patients(
    keyword: str,
    db: Session = Depends(get_db)
):
    """
    Tìm kiếm bệnh nhân theo tên,
    số điện thoại hoặc địa chỉ.
    """

    return (
        PatientService.search(
            db,
            keyword
        )
    )

#Chi tiết bệnh nhân
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    try:

        return (
            PatientService.get_patient(
                db,
                patient_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

#Tạo bệnh nhân
@router.post(
    "/",
    response_model=PatientResponse,
    dependencies=[Depends(AdminOnly)]
)
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db)
):
    try:

        return (
            PatientService.create_patient(
                db,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/create-with-user",
    response_model=PatientResponse,
    dependencies=[Depends(AdminOnly)]
)
def create_patient_with_user(
    data: PatientCreateWithUser,
    db: Session = Depends(get_db)
):
    try:

        return (
            PatientService
            .create_patient_with_user(
                db,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete(
    "/{patient_id}",
    dependencies=[Depends(AdminOnly)]
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """
    Xóa bệnh nhân.
    """

    try:

        PatientService.delete_patient(
            db,
            patient_id
        )

        return {
            "message":
                "Xóa bệnh nhân thành công"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
    dependencies=[Depends(AdminOnly)]
)
def update_patient(
    patient_id: int,
    data: PatientUpdate,
    db: Session = Depends(get_db)
):
    """
    Cập nhật bệnh nhân.
    """

    try:

        return (
            PatientService.update_patient(
                db,
                patient_id,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )