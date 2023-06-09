from asyncio import sleep
from datetime import date
from uuid import uuid4

from .conftest import create_test_auth_headers_for_user


employee_data_for_creation = {
    "employee_id": uuid4(),
    "name": "Alex",
    "surname": "Ivanov",
    "email": "chetkypacan@yandex.ru",
    "password": "12345",
    "current_salary": "150000.60",
    "next_promotion_date": date(2023, 8, 4),
}


async def test_get_employee_data_positive(client, create_employee_in_database):

    #  Preparation
    await create_employee_in_database(**employee_data_for_creation)
    headers = create_test_auth_headers_for_user(employee_data_for_creation["email"])

    response = client.get("/personal_account", headers=headers)

    data_from_response = response.json()

    assert response.status_code == 200
    assert (
        data_from_response["current_salary"]
        == employee_data_for_creation["current_salary"]
    )
    assert data_from_response["next_promotion_date"] == str(
        employee_data_for_creation["next_promotion_date"]
    )


async def test_get_employee_data_expired_token(client, create_employee_in_database):
    """Wait for the token to expire"""

    await create_employee_in_database(**employee_data_for_creation)
    headers = create_test_auth_headers_for_user(
        employee_data_for_creation["email"], wait_test=True
    )

    # Wait more expire param in jwt
    await sleep(2)  # Fix me

    response = client.get("/personal_account", headers=headers)

    data_from_response = response.json()

    assert response.status_code == 401
    assert data_from_response["detail"] == "Could not validate credentials"


async def test_get_employee_data_auth_error(client, create_employee_in_database):
    """Request without jwt-token"""

    await create_employee_in_database(**employee_data_for_creation)

    response = client.get("/personal_account")

    data_from_response = response.json()

    assert response.status_code == 401
    assert data_from_response["detail"] == "Not authenticated"


async def test_get_employee_data_bad_credentials(client, create_employee_in_database):
    """Request with invalid email in the jwt"""

    await create_employee_in_database(**employee_data_for_creation)
    headers = create_test_auth_headers_for_user(
        employee_data_for_creation["email"] + "a"
    )

    response = client.get("/personal_account", headers=headers)

    data_from_response = response.json()

    assert response.status_code == 401
    assert data_from_response["detail"] == "Could not validate credentials"


async def test_get_employee_data_invalid_token(client, create_employee_in_database):

    await create_employee_in_database(**employee_data_for_creation)
    headers: dict = create_test_auth_headers_for_user(
        employee_data_for_creation["email"]
    )
    headers["Authorization"] += "a"

    response = client.get("/personal_account", headers=headers)

    data_from_response = response.json()

    assert response.status_code == 401
    assert data_from_response["detail"] == "Could not validate credentials"
