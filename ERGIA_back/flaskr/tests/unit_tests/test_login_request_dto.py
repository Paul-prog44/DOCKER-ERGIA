import pytest
from pydantic import ValidationError
from flaskr.entities.users.login_request_dto import LoginRequestDTO
import os

os.environ['TESTING'] = 'True'

def test_valid_dto():
    """Test avec des données valides."""
    payload = {"email": "user@example.com", "password": "securepassword123"}
    dto = LoginRequestDTO(**payload)
    assert dto.email == "user@example.com"
    assert dto.password == "securepassword123"


def test_missing_email():
    """Test lorsque le champ email est manquant."""
    payload = {"password": "securepassword123"}
    with pytest.raises(ValidationError) as exc_info:
        LoginRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 1  # Une seule erreur pour le champ manquant
    assert errors[0]['loc'] == ('email',)
    assert errors[0]['msg'] == "Field required"
    assert errors[0]['type'] == "missing"


def test_missing_password():
    """Test lorsque le champ password est manquant."""
    payload = {"email": "user@example.com"}
    with pytest.raises(ValidationError) as exc_info:
        LoginRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 1  # Une seule erreur pour le champ manquant
    assert errors[0]['loc'] == ('password',)
    assert errors[0]['msg'] == "Field required"
    assert errors[0]['type'] == "missing"


def test_invalid_email_type():
    """Test avec un type incorrect pour le champ email."""
    payload = {"email": 123, "password": "securepassword123"}  # Erreur attendue sur email
    with pytest.raises(ValidationError) as exc_info:
        LoginRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 1  # Une seule erreur pour le type incorrect
    assert errors[0]['loc'] == ('email',)
    assert errors[0]['msg'] == "Input should be a valid string"
    assert errors[0]['type'] == "string_type"


def test_invalid_password_type():
    """Test avec un type incorrect pour le champ password."""
    payload = {"email": "user@example.com", "password": 12345}  # Erreur attendue sur password
    with pytest.raises(ValidationError) as exc_info:
        LoginRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 1  # Une seule erreur pour le type incorrect
    assert errors[0]['loc'] == ('password',)
    assert errors[0]['msg'] == "Input should be a valid string"
    assert errors[0]['type'] == "string_type"

