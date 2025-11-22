import pytest
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_login():

    response = client.post(
        "/login",
        json={
            "email": "test@example.com",
            "password": "testtest"
        }
    )
    
    # Vérifications
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure de la réponse
    assert 'token' in data
    assert 'access_token' in data['token']
    assert data['token']['token_type'] == "bearer"
    assert len(data['token']["access_token"]) > 0


def test_predict_endpoint_requires_authentication():
    
    # Essayer d'accéder à /predict SANS token
    response = client.post(
        "/predict",
        json={"text": "This is a test"}
    )
    
    # Vérifications
    # L'endpoint doit rejeter la requête (401 Unauthorized ou 403 Forbidden)
    assert response.status_code in [401, 403]
    
    # Vérifier qu'il y a un message d'erreur
    assert "detail" in response.json()