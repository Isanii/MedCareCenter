"""
doctors.py

API quản lý bác sĩ.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.doctor_service import (
    DoctorService
)

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    DoctorCreateWithUser
)

from app.dependencies.roles import (AdminOnly)

router = APIRouter(
    prefix="/api/v1/doctors",
    tags=["Doctors"]
)

#API Lấy Danh Sách
@router.get(
    "/",
    response_model=list[DoctorResponse],
    summary="Danh sách bác sĩ"
)
def get_all_doctors(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Danh sách bác sĩ có phân trang.
    """

    return (
        DoctorService.get_all_doctors(
            db,
            skip,
            limit
        )
    )

@router.get(
    "/search",
    response_model=list[DoctorResponse],
    summary="Tìm kiếm bác sĩ",
   description="""
    Tìm theo:

    - Họ tên
    - Email
    - Chuyên khoa
    - Kinh nghiệm
    """
)
def search_doctors(
    keyword: str | None = None,
    min_exp: int | None = None,
    db: Session = Depends(get_db)
):
    """
    Tìm kiếm bác sĩ.
    """

    return (
        DoctorService.search(
            db,
            keyword,
            min_exp
        )
    )

@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """
    Chi tiết bác sĩ.
    """

    try:

        return (
            DoctorService.get_doctor(
                db,
                doctor_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

#API Tạo bác sĩ
@router.post(
    "/",
    response_model=DoctorResponse,
    dependencies= [
        Depends(AdminOnly)
    ],
    status_code=201,
    summary="Tạo bác sĩ mới"
)
def create_doctor(
    data: DoctorCreate,
    db: Session = Depends(get_db)
):
    """
    Tạo bác sĩ mới.
    """

    try:

        return (
            DoctorService.create_doctor(
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
    response_model=DoctorResponse,
    status_code=201,
    summary="Tạo bác sĩ và tài khoản"
)
def create_doctor_with_user(
    data: DoctorCreateWithUser,
    db: Session = Depends(get_db)
):
    try:

        return (
            DoctorService
            .create_doctor_with_user(
                db,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )



#Cập nhật thông tin bác sĩ
@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse,
    dependencies=[
        Depends(AdminOnly)
    ],
    summary="Cập nhật bác sĩ"
)
def update_doctor(
    doctor_id: int,
    data: DoctorUpdate,
    db: Session = Depends(get_db)
):
    try:

        return (
            DoctorService.update_doctor(
                db,
                doctor_id,
                data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


#Xóa bác sĩ
@router.delete(
    "/{doctor_id}",
    dependencies=[
        Depends(AdminOnly)
    ],
    summary="Xóa bác sĩ"
)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    try:

        DoctorService.delete_doctor(
            db,
            doctor_id
        )

        return {
            "message":
                "Xóa bác sĩ thành công"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )