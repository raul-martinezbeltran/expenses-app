from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item_success():
    form_data = {"name": "lunch", "amount": "3.0"}
    response = client.post(f"create_expense/", data=form_data)
    assert response.status_code == 200
    assert response.json() == {"message": f"Expense {form_data["name"]} created"}

def test_create_item_failure():
    form_data = {"name": "lunch"}
    response = client.post(f"create_expense/", data=form_data)
    assert response.status_code == 422