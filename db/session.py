from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import constans

##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################


# Create async engine for interaction with database
engine = create_async_engine(constans.REAL_DATABASE_URL, future=True, echo=True)

# Create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
