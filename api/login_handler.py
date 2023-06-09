from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .auth.auth import auth_employee_by_pass_and_email
from .auth.auth import get_token
from .models import Token
from db.session import get_db_session

login_router = APIRouter()


@login_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> Optional[Token]:
    """
    Function for authenticate employee.
    Returns jwt-token if success.
    """
    employee = await auth_employee_by_pass_and_email(
        form_data.username, form_data.password, session
    )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token: Token = get_token(username=employee.email)

    return access_token
