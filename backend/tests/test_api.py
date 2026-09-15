from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_claim_analysis():
    claim = {
        'id': 'CLM-001',
        'policy_id': 'POL-100',
        'claimant': 'Test User',
        'claim_type': 'property',
        'description': 'Water damage with missing receipt',
        'estimated_loss': 12000,
        'location': 'Lahore',
        'evidence': ['receipt_missing.jpg']
    }
    created = client.post('/claims', json=claim)
    assert created.status_code == 200
    analysis = client.post('/claims/CLM-001/analyze')
    assert analysis.status_code == 200
    data = analysis.json()
    assert data['severity'] == 'medium'
    assert data['human_review_required'] is True
    assert data['risk_score'] > 0
