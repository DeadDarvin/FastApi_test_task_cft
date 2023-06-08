from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ShowEmployeeData
from db.dals import EmployeeDAL
from db.session import get_db_session


employee_router = APIRouter()


async def _get_employee_salary_and_promotion_by_id(
    employee_id: UUID, session: AsyncSession
) -> Optional[ShowEmployeeData]:
    async with session.begin():
        employee_dal = EmployeeDAL(session)
        employee = await employee_dal.get_employee_by_id(employee_id)

        if employee is not None:
            return ShowEmployeeData(
                current_salary=str(employee.current_salary),
                next_promotion_date=str(employee.next_promotion_date),
            )


@employee_router.get("/salary", response_model=ShowEmployeeData)
async def get_employee_salary_and_promotion_by_id(
    employee_id: UUID, session: AsyncSession = Depends(get_db_session)
) -> Optional[ShowEmployeeData]:
    employee_data = await _get_employee_salary_and_promotion_by_id(employee_id, session)
    if employee_data is None:
        raise HTTPException(
            status_code=404, detail=f"Employee with id {employee_id} not found"
        )

    return employee_data
