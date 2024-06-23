# tests/test_api.py

from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_calculate():
    response = client.post("/calculate/", json={"expression": "3 4 +"})
    assert response.status_code == 200
    assert response.json() == {"expression": "3 4 +", "result": 7}

def test_export_csv():
    response = client.get("/export_csv/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv"
