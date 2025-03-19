from datetime import date
from datetime import timedelta


async def test_delete_leave_invalid_id(client):
    leave_id = -1

    response = client.delete(f"/leaves/{leave_id}/")
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "ID отпуска должен быть целым неотрицательным числом"
    )


async def test_delete_leave_not_found(client):
    leave_id = 228

    response = client.delete(f"/leaves/{leave_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Отпуск не найден"


async def test_delete_leave_success(client):
    leave_data = {
        "employee_id": 1,
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=5)),
    }
    create_response = client.post("/leaves/", json=leave_data)
    assert create_response.status_code == 200
    leave_id = create_response.json()["id"]

    delete_response = client.delete(f"/leaves/{leave_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "Отпуск удален"}

    response = client.delete(f"/leaves/{leave_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Отпуск не найден"
