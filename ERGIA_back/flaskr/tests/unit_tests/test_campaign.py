import pytest
from flaskr.main import create_app
import os

os.environ['TESTING'] = 'True'

@pytest.fixture
def client():
    #Création app en mode test
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client  # Donne accès au client dans le test

def test_campaigns_endpoint(client):
    """Test l'endpoint /campaigns"""
    response = client.get('/campaigns')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_campaigns5_endpoint(client):
    """Test l'endpoint /campaigns/5"""
    response = client.get('/campaigns/5')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_add_user_to_campaign_with_missing_prop(client):
    """Test l'ajout d'un utilisateur à une campagne avec des propriétés manquantes"""
    payload = {
        "user_id": 9
    }
    response = client.post('/add_user_to_campaign', json=payload, content_type='application/json')
    assert response.status_code == 400

