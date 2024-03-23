import pytest
from app import app
from keyManager import initialize_database

# creating a reusable test component that can be used as arguments in test functions
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

# tests the endpoint of client
def test_jwks_endpoint(client):
    response = client.get('/.well-known/jwks.json')
    data = response.get_json()
    assert response.status_code == 200
    assert 'keys' in data
    for key in data['keys']:
        assert all(k in key for k in ('kty', 'use', 'kid', 'n', 'e'))

# tests the authentication endpoint of client
def test_auth_endpoint(client):
    response = client.post('/auth')
    data = response.get_json()
    assert response.status_code == 200
    assert 'token' in data
