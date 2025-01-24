import pytest
from flaskr.entities.users.update_password_request_dto import UpdatePasswordRequestDTO  # Remplacez par le chemin réel
import os

os.environ['TESTING'] = 'True'

def test_valid_dto():
    """Test avec des données valides."""
    dto = UpdatePasswordRequestDTO(old_password="oldpass123", new_password="newpass456")
    assert dto.old_password == "oldpass123"
    assert dto.new_password == "newpass456"


def test_missing_old_password():
    """Test lorsque le champ old_password est manquant."""
    with pytest.raises(TypeError) as exc_info:
        UpdatePasswordRequestDTO(new_password="newpass456")
    assert "__init__() missing 1 required positional argument: 'old_password'" in str(exc_info.value)


def test_missing_new_password():
    """Test lorsque le champ new_password est manquant."""
    with pytest.raises(TypeError) as exc_info:
        UpdatePasswordRequestDTO(old_password="oldpass123")
    assert "__init__() missing 1 required positional argument: 'new_password'" in str(exc_info.value)

def test_extra_field():
    """Test avec des champs supplémentaires non attendus."""
    with pytest.raises(TypeError) as exc_info:
        UpdatePasswordRequestDTO(old_password="oldpass123", new_password="newpass456", extra_field="unexpected")
    assert "__init__() got an unexpected keyword argument 'extra_field'" in str(exc_info.value)
