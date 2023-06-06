from uuid import UUID

from sqlalchemy import select

from .model import Employee


class EmployeeDAL:
    """For interaction with DB"""

    def __init__(self, session):
        self.session = session

    async def get_employee_by_id(self, employee_id: UUID):
        query = select(Employee).where(Employee.employee_id == employee_id)
        result = await self.session.execute(query)
        print(result)
        employee_row = result.fetchone()
        print(employee_row)
        if employee_row is not None:
            return employee_row[0]
