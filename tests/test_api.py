from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_logistics():
    resp = client.post("/predict", json={"text": "Blue Dart courier charges for warehouse"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "Logistics"
    assert 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["top_keywords"], list)
    assert len(data["top_keywords"]) > 0

def test_predict_cloud():
    resp = client.post("/predict", json={"text": "AWS monthly cloud hosting bill"})
    assert resp.status_code == 200
    assert resp.json()["category"] == "Cloud/Software"

def test_predict_empty():
    resp = client.post("/predict", json={"text": ""})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()

def test_predict_whitespace():
    resp = client.post("/predict", json={"text": "   "})
    assert resp.status_code == 400

def test_predict_long_text():
    long_text = "courier " * 500  # 500 times
    resp = client.post("/predict", json={"text": long_text})
    assert resp.status_code == 200
    assert resp.json()["category"] == "Logistics"

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"