# tests/test_app.py
import pytest
from app import app, keysStorage 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_jwks_endpoint(client):
    """Test the JWKS endpoint for a successful response."""
    rv = client.get('/.well-known/jwks.json')
    assert rv.status_code == 200
    assert 'keys' in rv.json
    assert len(rv.json['keys']) > 0 

def test_auth_endpoint_success(client):
    """Test the auth endpoint for a successful token generation."""
    rv = client.post('/auth')
    assert rv.status_code == 200
    assert 'token' in rv.json

def test_auth_endpoint_with_expired(client):
    """Test the auth endpoint to ensure it handles expired keys correctly."""
    rv = client.post('/auth?expired=true')
    assert rv.status_code == 400 or 'error' in rv.json

