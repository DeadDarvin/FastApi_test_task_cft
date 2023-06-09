from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import ShowEmployeeData
from ..models import Token
from .hashing import verify_password
from .token import create_access_token
from .token import get_email_from_jwt
from constans import TOKEN_TYPE
from db.dals import EmployeeDAL
from db.model import Employee
from db.session import get_db_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


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


async def get_current_employee_from_token(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db_session)
) -> Optional[ShowEmployeeData]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    email = get_email_from_jwt(token)
    if email is None:
        #  logger.warning!!!!!!
        print("!!!!!!INVALID TOKEN!!!!!!!!")
        raise credentials_exception

    employee = await _get_employee_by_email_for_auth(email, session)
    if employee is None:
        raise credentials_exception

    return employee
