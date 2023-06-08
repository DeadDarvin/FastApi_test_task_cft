from datetime import date
from uuid import uuid4

import pytest


HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "accept": "application/json",
}

employee_data_for_creation = {
    "employee_id": uuid4(),
    "name": "Alex",
    "surname": "Ivanov",
    "email": "chetkypacan@yandex.ru",
    "password": "12345",
    "current_salary": "150000.60",
    "next_promotion_date": date(2023, 8, 4),
}


async def test_login_handler_positive(client, create_employee_in_database):
    #  Preparation

    await create_employee_in_database(**employee_data_for_creation)

    employee_data_for_request = {
        "username": employee_data_for_creation["email"],
        "password": employee_data_for_creation["password"],
    }

    response = client.post("/auth", headers=HEADERS, data=employee_data_for_request)

    data_from_response = response.json()

    assert response.status_code == 200
    assert data_from_response.get("access_token") is not None
    assert data_from_response["token_type"] == "bearer"


@pytest.mark.parametrize(
    "data_for_request, expected_status_code, expected_detail",
    [
        (
            {
                "username": employee_data_for_creation["email"],
                "password": employee_data_for_creation["password"] + "invalid_anchor",
            },
            401,
            {"detail": "Incorrect username or password"},
        ),
        (
            {
                "username": employee_data_for_creation["email"] + "invalid_anchor",
                "password": employee_data_for_creation["password"],
            },
            401,
            {"detail": "Incorrect username or password"},
        ),
        (
            {
                "username": employee_data_for_creation["email"] + "invalid_anchor",
                "password": employee_data_for_creation["password"] + "invalid_anchor",
            },
            401,
            {"detail": "Incorrect username or password"},
        ),
    ],
)
async def test_login_handler_invalid_data(
    client,
    create_employee_in_database,
    data_for_request,
    expected_status_code,
    expected_detail,
):

    await create_employee_in_database(**employee_data_for_creation)

    response = client.post("/auth", headers=HEADERS, data=data_for_request)

    data_from_response = response.json()

    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail


@pytest.mark.parametrize(
    "data_for_request, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "username"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "password"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
        (
            {"username": "test_username"},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "password"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            {"password": "test_password"},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "username"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
    ],
)
async def test_login_handler_negative(
    client, data_for_request, expected_status_code, expected_detail
):
    response = client.post("/auth", headers=HEADERS, data=data_for_request)

    data_from_response = response.json()

    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail
