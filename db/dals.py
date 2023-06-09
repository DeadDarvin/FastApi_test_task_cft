from typing import Optional

from sqlalchemy import select

from .model import Employee


class EmployeeDAL:
    """For interaction with DB"""

    def __init__(self, session):
        self.session = session

    async def get_employee_by_email(self, email: str) -> Optional[Employee]:
        query = select(Employee).where(Employee.email == email)
        result = await self.session.execute(query)
        employee_row = result.fetchone()
        if employee_row is not None:
            return employee_row[0]
