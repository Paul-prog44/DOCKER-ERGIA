import pytest
from pydantic import ValidationError
from flaskr.entities.corpus.corpus_response_dto import CorpusResponseDTO  # Remplacez par le chemin réel
import os

os.environ['TESTING'] = 'True'

def test_valid_dto():
    """Test avec des données valides."""
    payload = {
        "id_original_text": 123,
        "path": "/path/to/resource",
        "campaign_id": 456
    }
    dto = CorpusResponseDTO(**payload)
    assert dto.id_original_text == 123
    assert dto.path == "/path/to/resource"
    assert dto.campaign_id == 456


def test_missing_required_fields():
    """Test lorsque des champs obligatoires manquent."""
    payload = {
        "id_original_text": 123
    }
    with pytest.raises(ValidationError) as exc_info:
        CorpusResponseDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 2  # Deux champs manquent
    assert any(error['loc'] == ('path',) for error in errors)
    assert any(error['loc'] == ('campaign_id',) for error in errors)


def test_invalid_field_types():
    """Test avec des types de champs invalides."""
    payload = {
        "id_original_text": "not-an-int",  # Erreur attendue
        "path": 123,  # Erreur attendue
        "campaign_id": "not-an-int"  # Erreur attendue
    }
    with pytest.raises(ValidationError) as exc_info:
        CorpusResponseDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 3  # Trois erreurs de type
    assert any(error['loc'] == ('id_original_text',) for error in errors)
    assert any(error['loc'] == ('path',) for error in errors)
    assert any(error['loc'] == ('campaign_id',) for error in errors)

def test_empty_payload():
    """Test avec un payload vide."""
    payload = {}
    with pytest.raises(ValidationError) as exc_info:
        CorpusResponseDTO(**payload)
    errors = exc_info.value.errors()
    assert len(errors) == 3  # Tous les champs manquent
    assert any(error['loc'] == ('id_original_text',) for error in errors)
    assert any(error['loc'] == ('path',) for error in errors)
    assert any(error['loc'] == ('campaign_id',) for error in errors)
