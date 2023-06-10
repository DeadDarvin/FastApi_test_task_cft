from datetime import date
from uuid import uuid4

import psycopg2
from passlib.context import CryptContext

from custom_logger import get_custom_loger

logger = get_custom_loger("migrate")


def get_hash_from_password(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


employee_data_for_creation = {
    "employee_id": str(uuid4()),
    "name": "Alex",
    "surname": "Ivanov",
    "email": "chetkypacan@yandex.ru",
    "hashed_password": get_hash_from_password("12345"),
    "current_salary": "150000.60",
    "next_promotion_date": date(2023, 8, 4),
}


def create_employee_in_database(data_for_record: tuple):
    try:
        logger.info(msg=f"Create employee with data {data_for_record} in DB")
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="0.0.0.0",
            port="5444",
        )

        query = """INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s);"""

        curs = conn.cursor()
        curs.execute(query, data_for_record)
        conn.commit()

    except (Exception, psycopg2.Error):
        logger.error("Failed to insert record into mobile table", exc_info=True)

    finally:
        if conn:
            curs.close()
            conn.close()
            logger.info("PostgreSQL connection is closed")


if __name__ == "__main__":
    create_employee_in_database(tuple(employee_data_for_creation.values()))
