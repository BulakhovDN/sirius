from datetime import date
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import LeaveCreate
from api.models import LeaveResponse
from db.database import get_db
from db.service_layer import LeaveService

router = APIRouter()


@router.post("/leaves/", response_model=LeaveResponse)
async def create_leave(leave: LeaveCreate, db: AsyncSession = Depends(get_db)):
    service = LeaveService(db)
    return await service.create_leave(leave)


@router.get("/leaves/{employee_id}/recent", response_model=List[LeaveResponse])
async def get_recent_leaves(employee_id: int, db: AsyncSession = Depends(get_db)):
    service = LeaveService(db)
    return await service.get_recent_leaves(employee_id)


@router.get("/leaves/", response_model=List[LeaveResponse])
async def get_leaves(
    start_date: date, end_date: date, db: AsyncSession = Depends(get_db)
):
    service = LeaveService(db)
    return await service.get_leaves_by_date_range(start_date, end_date)


@router.delete("/leaves/{leave_id}")
async def delete_leave(leave_id: int, db: AsyncSession = Depends(get_db)):
    service = LeaveService(db)
    return await service.delete_leave(leave_id)
