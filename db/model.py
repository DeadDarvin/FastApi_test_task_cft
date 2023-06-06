import uuid

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


##############################
# BLOCK WITH DATABASE MODELS #
##############################


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=60), nullable=False)
    surname = Column(String(length=60), nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    current_salary = Column(Numeric(precision=8, scale=2), nullable=False)
    next_promotion_date = Column(Date, nullable=False)
