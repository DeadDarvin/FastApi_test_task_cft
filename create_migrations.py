import os


def main():
    root = os.getcwd()

    # Create migrations in real DB
    os.system('alembic revision --autogenerate -m "running migrations"')
    os.system("alembic upgrade heads")

    os.chdir(f"{root}/tests/")

    # Create migrations in real test DB
    os.system(
        f'PYTHONPATH={root} alembic revision --autogenerate -m "tests running migrations"'
    )
    os.system(f"PYTHONPATH={root} alembic upgrade heads")

    os.chdir(f"{root}")


if __name__ == "__main__":
    main()
