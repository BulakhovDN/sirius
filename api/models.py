from datetime import date

from pydantic import BaseModel


class LeaveCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date


class LeaveResponse(LeaveCreate):
    id: int

    class Config:
        orm_mode = True
