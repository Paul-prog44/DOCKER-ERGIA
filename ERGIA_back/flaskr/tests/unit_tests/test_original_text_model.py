from unittest.mock import patch, MagicMock
import pytest
from flaskr.models.original_text_model import OriginalTextModel

class TestOriginalTextModel:

    @patch("flaskr.models.original_text_model.db_singleton")
    def test_get_all_original_texts(self, mock_db_singleton):
        """Test récupération de tous les textes originaux."""
        mock_execute_query = MagicMock(return_value=[{"id": 1, "path": "path1"}])
        mock_db_singleton.execute_query = mock_execute_query

        original_text_model = OriginalTextModel()
        result = original_text_model.get_all_original_texts()

        expected_query = "SELECT * FROM original_texts;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query)
        assert result == [{"id": 1, "path": "path1"}]

    @patch("flaskr.models.original_text_model.db_singleton")
    def test_get_original_text(self, mock_db_singleton):
        """Test récupération d'un texte original par ID."""
        mock_execute_query = MagicMock(return_value={"id": 1, "path": "path1"})
        mock_db_singleton.execute_query = mock_execute_query

        original_text_model = OriginalTextModel()
        id_original_text = 1
        result = original_text_model.get_original_text(id_original_text)

        expected_query = "SELECT * FROM original_texts WHERE id_original_text = %s;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, (id_original_text,))
        assert result == {"id": 1, "path": "path1"}

    @patch("flaskr.models.original_text_model.db_singleton")
    def test_create_original_text(self, mock_db_singleton):
        """Test création d'un texte original."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        original_text_model = OriginalTextModel()
        result = original_text_model.create_original_text(path="path/to/file", campaign_id=42)

        expected_query = """
            INSERT INTO original_texts (path, campaign_id)
            VALUES (%s, %s);
        """
        expected_params = ("path/to/file", 42)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.original_text_model.db_singleton")
    def test_update_original_text_all_fields(self, mock_db_singleton):
        """Test mise à jour d'un texte original avec tous les champs."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        original_text_model = OriginalTextModel()
        result = original_text_model.update_original_text(
            id_original_text=1,
            path="new/path/to/file",
            campaign_id=84,
        )

        expected_query = """
            UPDATE original_texts
            SET path = %s, campaign_id = %s
            WHERE id_original_text = %s;
        """
        expected_params = ("new/path/to/file", 84, 1)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.original_text_model.db_singleton")
    def test_update_original_text_some_fields(self, mock_db_singleton):
        """Test mise à jour d'un texte original avec certains champs uniquement."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        original_text_model = OriginalTextModel()
        result = original_text_model.update_original_text(
            id_original_text=1,
            path="partial/update/path",
        )

        expected_query = """
            UPDATE original_texts
            SET path = %s
            WHERE id_original_text = %s;
        """
        expected_params = ("partial/update/path", 1)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.original_text_model.db_singleton")
    def test_update_original_text_no_updates(self, mock_db_singleton):
        """Test mise à jour sans aucun champ modifié."""
        mock_execute_query = MagicMock()
        mock_db_singleton.execute_query = mock_execute_query

        original_text_model = OriginalTextModel()
        result = original_text_model.update_original_text(id_original_text=1)

        mock_db_singleton.execute_query.assert_not_called()
        assert result is None

    @patch("flaskr.models.original_text_model.db_singleton")
    def test_delete_original_text(self, mock_db_singleton):
        """Test suppression d'un texte original."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        original_text_model = OriginalTextModel()
        result = original_text_model.delete_original_text(id_original_text=1)

        expected_query = "DELETE FROM original_texts WHERE id_original_text = %s;"
        expected_params = (1,)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"
