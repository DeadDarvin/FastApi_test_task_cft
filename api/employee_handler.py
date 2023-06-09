from typing import Optional

from fastapi import Depends
from fastapi.routing import APIRouter

from .auth.auth import get_current_employee_from_token
from .models import ShowEmployeeData
from db.model import Employee

employee_router = APIRouter()


def _get_employee_salary_and_promotion_from_employee(
    current_employee: Employee,
) -> ShowEmployeeData:
    return ShowEmployeeData(
        current_salary=str(current_employee.current_salary),
        next_promotion_date=str(current_employee.next_promotion_date),
    )


@employee_router.get("/personal_account", response_model=ShowEmployeeData)
async def get_employee_salary_and_promotion(
    current_employee: Employee = Depends(get_current_employee_from_token),
) -> Optional[ShowEmployeeData]:

    current_employee_data = _get_employee_salary_and_promotion_from_employee(
        current_employee
    )
    return current_employee_data
