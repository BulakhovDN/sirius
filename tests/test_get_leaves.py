from datetime import date
from datetime import timedelta


async def test_get_leaves_valid_dates(client):
    leave_data = {
        "employee_id": 1,
        "start_date": str(date.today() - timedelta(days=10)),
        "end_date": str(date.today()),
    }
    create_response = client.post("/leaves/", json=leave_data)
    assert create_response.status_code == 200

    response = client.get(
        f"/leaves/?start_date={leave_data['start_date']}&end_date={leave_data['end_date']}"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["employee_id"] == 1


async def test_get_leaves_start_date_before_end_date(client):
    start_date = str(date.today())
    end_date = str(date.today() - timedelta(days=5))

    response = client.get(f"/leaves/?start_date={start_date}&end_date={end_date}")

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Дата начала отпуска должна быть раньше даты окончания"
    )


async def test_get_leaves_no_leaves_in_period(client):
    start_date = str(date.today() - timedelta(days=30))
    end_date = str(date.today() - timedelta(days=20))

    response = client.get(f"/leaves/?start_date={start_date}&end_date={end_date}")

    assert response.status_code == 404
    assert (
        response.json()["detail"] == "Не найдено ни одного отпуска за указанный период"
    )
