from datetime import date

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.handler_validator import LeaveValidator
from db.models import Leave


class LeaveService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_leave(self, leave_data):
        LeaveValidator.validate_employee_id(leave_data.employee_id)
        LeaveValidator.validate_dates(leave_data.start_date, leave_data.end_date)

        async with self.db.begin():
            stmt = select(Leave).filter(
                Leave.employee_id == leave_data.employee_id,
                Leave.start_date <= leave_data.end_date,
                Leave.end_date >= leave_data.start_date,
            )
            result = await self.db.execute(stmt)
            if result.scalars().first():
                raise HTTPException(
                    status_code=400,
                    detail="Этот период отпуска пересекается с существующим",
                )

            new_leave = Leave(
                employee_id=leave_data.employee_id,
                start_date=leave_data.start_date,
                end_date=leave_data.end_date,
            )
            self.db.add(new_leave)

            return new_leave

    async def get_recent_leaves(self, employee_id: int):
        LeaveValidator.validate_employee_id(employee_id)

        async with self.db.begin():
            stmt = (
                select(Leave)
                .filter(Leave.employee_id == employee_id)
                .order_by(Leave.start_date.desc())
                .limit(3)
            )
            result = await self.db.execute(stmt)
            leaves = result.scalars().all()

            if not leaves:
                raise HTTPException(
                    status_code=404, detail="Отпусков для данного сотрудника не найдено"
                )

            return leaves

    async def get_leaves_by_date_range(self, start_date: date, end_date: date):
        LeaveValidator.validate_dates(start_date, end_date)

        async with self.db.begin():
            stmt = select(Leave).filter(
                Leave.start_date >= start_date, Leave.end_date <= end_date
            )
            result = await self.db.execute(stmt)
            leaves = result.scalars().all()

            if not leaves:
                raise HTTPException(
                    status_code=404,
                    detail="Не найдено ни одного отпуска за указанный период",
                )

            return leaves

    async def delete_leave(self, leave_id: int):
        LeaveValidator.validate_leave_id(leave_id)

        async with self.db.begin():
            stmt = select(Leave).filter(Leave.id == leave_id)
            result = await self.db.execute(stmt)
            leave = result.scalars().first()

            if not leave:
                raise HTTPException(status_code=404, detail="Отпуск не найден")

            await self.db.execute(delete(Leave).where(Leave.id == leave_id))
            return {"detail": "Отпуск удален"}
