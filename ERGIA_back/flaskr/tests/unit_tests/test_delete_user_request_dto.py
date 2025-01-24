import pytest
from pydantic import ValidationError
from flaskr.entities.users.delete_user_request_dto import DeleteUserRequestDTO  # Remplacez par le chemin réel
import os

os.environ['TESTING'] = 'True'

def test_valid_dto():
    """Test avec des données valides."""
    payload = {"email": "user@example.com"}
    dto = DeleteUserRequestDTO(**payload)
    assert dto.email == "user@example.com"


def test_missing_email():
    """Test lorsque le champ email est manquant."""
    payload = {}
    with pytest.raises(ValidationError) as exc_info:
        DeleteUserRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 1  # Une seule erreur pour le champ manquant
    assert errors[0]['loc'] == ('email',)
    assert errors[0]['msg'] == "Field required"
    assert errors[0]['type'] == "missing"


def test_invalid_email_type():
    """Test avec un type incorrect pour le champ email."""
    payload = {"email": 123}  # Erreur attendue
    with pytest.raises(ValidationError) as exc_info:
        DeleteUserRequestDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 1  # Une seule erreur pour le type incorrect
    assert errors[0]['loc'] == ('email',)
    assert errors[0]['msg'] == "Input should be a valid string"
    assert errors[0]['type'] == "string_type"