import pytest
from pydantic import ValidationError
from flaskr.entities.users.create_user_request_dto import CreateUserRequestDTO 
import os

os.environ['TESTING'] = 'True'

def test_valid_dto():
    """Test avec des données valides."""
    payload = {
        "email": "user@example.com",
        "password": "securepassword123",
        "firstname": "John",
        "lastname": "Doe",
        "acceptCgu": True
    }
    dto = CreateUserRequestDTO(**payload)
    assert dto.email == "user@example.com"
    assert dto.password == "securepassword123"
    assert dto.firstname == "John"
    assert dto.lastname == "Doe"
    assert dto.acceptCgu is True


def test_missing_required_fields():
    """Test lorsque des champs obligatoires manquent."""
    payload = {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 3  # firstname, lastname, acceptCgu manquent
    assert any(error['loc'] == ('firstname',) for error in errors)
    assert any(error['loc'] == ('lastname',) for error in errors)
    assert any(error['loc'] == ('acceptCgu',) for error in errors)


def test_invalid_field_types():
    """Test avec des types de champs invalides."""
    payload = {
        "email": 123,  # Erreur attendue
        "password": False,  # Erreur attendue
        "firstname": True,  # Erreur attendue
        "lastname": 456,  # Erreur attendue
    }
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 5   # Tous les champs ont des types incorrects
    assert any(error['loc'] == ('email',) for error in errors)
    assert any(error['loc'] == ('password',) for error in errors)
    assert any(error['loc'] == ('firstname',) for error in errors)
    assert any(error['loc'] == ('lastname',) for error in errors)


def test_empty_payload():
    """Test avec un payload vide."""
    payload = {}
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 5  # Tous les champs obligatoires manquent
    assert any(error['loc'] == ('email',) for error in errors)
    assert any(error['loc'] == ('password',) for error in errors)
    assert any(error['loc'] == ('firstname',) for error in errors)
    assert any(error['loc'] == ('lastname',) for error in errors)
    assert any(error['loc'] == ('acceptCgu',) for error in errors)
