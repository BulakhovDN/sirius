from datetime import date
from datetime import timedelta


async def test_create_leave_valid_data(client):
    response = client.post(
        "/leaves/",
        json={
            "employee_id": 1,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=5)),
        },
    )
    assert response.status_code == 200
    assert response.json()["employee_id"] == 1


async def test_create_leave_invalid_employee_id(client):
    response = client.post(
        "/leaves/",
        json={
            "employee_id": -1,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=5)),
        },
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "ID сотрудника должен быть целым неотрицательным числом"
    )


async def test_create_leave_invalid_date_format(client):
    response = client.post(
        "/leaves/",
        json={"employee_id": 1, "start_date": "2025-13-01", "end_date": "2025-01-10"},
    )
    assert response.status_code == 422


async def test_create_leave_start_date_after_end_date(client):
    response = client.post(
        "/leaves/",
        json={
            "employee_id": 1,
            "start_date": str(date.today() + timedelta(days=5)),
            "end_date": str(date.today()),
        },
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Дата начала отпуска должна быть раньше даты окончания"
    )


async def test_create_leave_overlapping_dates(client):
    leave_data = {
        "employee_id": 2,
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=5)),
    }

    response = client.post("/leaves/", json=leave_data)
    assert response.status_code == 200

    response = client.post("/leaves/", json=leave_data)
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Этот период отпуска пересекается с существующим"
    )
