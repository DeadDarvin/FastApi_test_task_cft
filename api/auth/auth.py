from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Token
from .hashing import verify_password
from .token import create_access_token
from constans import TOKEN_TYPE
from db.dals import EmployeeDAL
from db.model import Employee


def get_token(username: str) -> Token:
    jwt: str = create_access_token(username)
    return Token(access_token=jwt, token_type=TOKEN_TYPE)


async def _get_employee_by_email_for_auth(
    email: str, session: AsyncSession
) -> Optional[Employee]:
    async with session.begin():
        employee_dal = EmployeeDAL(session)
        return await employee_dal.get_employee_by_email(email)


async def auth_employee_by_pass_and_email(
    email: str, password: str, session: AsyncSession
) -> Optional[Employee]:
    """
    Check employee with given email existence.
    And password correctness.
    """
    employee = await _get_employee_by_email_for_auth(email, session)
    if employee is None:
        return

    if not verify_password(password, employee.hashed_password):
        return

    return employee
