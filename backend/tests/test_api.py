from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_claim_analysis_routes_high_value_claim_to_specialist():
    claim = {
        "id": "CLM-001",
        "claimant_name": "Test Claimant",
        "claim_type": "property",
        "description": "Water damage to kitchen",
        "claimed_amount": 30000,
        "evidence_count": 3,
    }
    created = client.post("/claims", json=claim)
    assert created.status_code == 200

    result = client.post("/claims/CLM-001/analyze")
    assert result.status_code == 200
    body = result.json()
    assert body["severity"] == "high"
    assert body["route"] == "specialist_review"
    assert body["human_review_required"] is True


def test_missing_evidence_creates_signal():
    claim = {
        "id": "CLM-002",
        "claimant_name": "Test Claimant",
        "claim_type": "auto",
        "description": "Vehicle damage",
        "claimed_amount": 1000,
        "evidence_count": 0,
    }
    client.post("/claims", json=claim)
    result = client.post("/claims/CLM-002/analyze")
    assert result.status_code == 200
    assert result.json()["risk_signals"][0]["code"] == "NO_EVIDENCE"
