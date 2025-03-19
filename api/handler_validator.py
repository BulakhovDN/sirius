from fastapi import HTTPException


class LeaveValidator:
    @staticmethod
    def validate_employee_id(employee_id: int):
        if not isinstance(employee_id, int) or employee_id < 0:
            raise HTTPException(
                status_code=400,
                detail="ID сотрудника должен быть целым неотрицательным числом",
            )

    @staticmethod
    def validate_dates(start_date, end_date):
        if start_date >= end_date:
            raise HTTPException(
                status_code=400,
                detail="Дата начала отпуска должна быть раньше даты окончания",
            )

    @staticmethod
    def validate_leave_id(leave_id: int):
        if not isinstance(leave_id, int) or leave_id < 0:
            raise HTTPException(
                status_code=400,
                detail="ID отпуска должен быть целым неотрицательным числом",
            )
