from datetime import date
from datetime import timedelta


async def test_get_recent_leaves_valid_employee_id(client):
    employee_id = 1

    leave_dates = [
        (date.today() - timedelta(days=30), date.today() - timedelta(days=25)),
        (date.today() - timedelta(days=20), date.today() - timedelta(days=15)),
        (date.today() - timedelta(days=10), date.today() - timedelta(days=5)),
    ]

    for start_date, end_date in leave_dates:
        leave_data = {
            "employee_id": employee_id,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }
        create_response = client.post("/leaves/", json=leave_data)
        assert create_response.status_code == 200

    response = client.get(f"/leaves/{employee_id}/recent/")

    assert response.status_code == 200
    leaves = response.json()
    assert isinstance(leaves, list)
    assert len(leaves) == 3

    start_dates = [leave["start_date"] for leave in leaves]
    expected_dates = [
        str(d[0]) for d in sorted(leave_dates, key=lambda x: x[0], reverse=True)
    ]
    assert start_dates == expected_dates


async def test_get_recent_leaves_invalid_employee_id(client):
    response = client.get("/leaves/-1/recent/")

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "ID сотрудника должен быть целым неотрицательным числом"
    )


async def test_get_recent_leaves_no_leaves(client):
    employee_id = 2

    response = client.get(f"/leaves/{employee_id}/recent/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Отпусков для данного сотрудника не найдено"
