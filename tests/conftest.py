import asyncio
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Generator

import asyncpg
import pytest
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import constans
from api.auth.token import create_access_token
from db.session import get_db_session
from main import app

CLEAN_TABLE = "employee"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(constans.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            await session.execute(f"""TRUNCATE TABLE {CLEAN_TABLE};""")


##########################
# OUR TEST CLIENT #
##########################


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            constans.TEST_DATABASE_URL, future=True, echo=True
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db_session] = _get_test_db
    with TestClient(app) as client:
        yield client


##########################
# UTILS FOR TESTS #
##########################


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(constans.TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    pool.close()


@pytest.fixture
async def create_employee_in_database(asyncpg_pool):
    def get_hash_from_password(password: str) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    async def create_employee_in_database(
        employee_id: str,
        name: str,
        surname: str,
        email: str,
        password: str,
        current_salary: str,
        next_promotion_date: date,
    ):
        hashed_password: str = get_hash_from_password(password)

        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO employee VALUES ($1, $2, $3, $4, $5, $6, $7);""",
                employee_id,
                name,
                surname,
                email,
                hashed_password,
                current_salary,
                next_promotion_date,
            )

    return create_employee_in_database


def create_test_auth_headers_for_user(email: str, wait_test=False) -> dict[str, str]:

    expire = datetime.utcnow() + timedelta(seconds=1) if wait_test else None

    access_token = create_access_token(email, expire)
    return {"Authorization": f"Bearer {access_token}"}
