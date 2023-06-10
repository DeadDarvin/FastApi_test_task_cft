import os

from custom_logger import get_custom_loger

logger = get_custom_loger("create_migrations")


def main():
    root = os.getcwd()

    logger.info("Create migration in real DB")

    os.system('alembic revision --autogenerate -m "running migrations"')
    os.system("alembic upgrade heads")

    os.chdir(f"{root}/tests/")

    logger.info("Create migration in test DB")

    os.system(
        f'PYTHONPATH={root} alembic revision --autogenerate -m "tests running migrations"'
    )
    os.system(f"PYTHONPATH={root} alembic upgrade heads")

    os.chdir(f"{root}")
    logger.info("Migrations has been created")


if __name__ == "__main__":
    main()
