from unittest.mock import patch, MagicMock
import pytest
from flaskr.models.summary_model import SummaryModel

class TestSummaryModel:

    @patch("flaskr.models.summary_model.db_singleton")
    def test_get_all_summaries(self, mock_db_singleton):
        """Test récupération de tous les résumés."""
        mock_execute_query = MagicMock(return_value=[{"id_summary": 1, "path": "path/to/summary"}])
        mock_db_singleton.execute_query = mock_execute_query

        summary_model = SummaryModel()
        result = summary_model.get_all_summaries()

        expected_query = "SELECT * FROM summaries;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query)
        assert result == [{"id_summary": 1, "path": "path/to/summary"}]

    @patch("flaskr.models.summary_model.db_singleton")
    def test_get_summary(self, mock_db_singleton):
        """Test récupération d'un résumé par ID."""
        mock_execute_query = MagicMock(return_value={"id_summary": 1, "path": "path/to/summary"})
        mock_db_singleton.execute_query = mock_execute_query

        summary_model = SummaryModel()
        id_summary = 1
        result = summary_model.get_summary(id_summary)

        expected_query = "SELECT * FROM summaries WHERE id_summary = %s;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, (id_summary,))
        assert result == {"id_summary": 1, "path": "path/to/summary"}

    @patch("flaskr.models.summary_model.db_singleton")
    def test_create_summary(self, mock_db_singleton):
        """Test création d'un résumé."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        summary_model = SummaryModel()
        result = summary_model.create_summary(
            path="path/to/summary",
            original_text_id=10,
            annotator_id=5,
            ia_generated=True
        )

        expected_query = """
            INSERT INTO summaries (path, original_text_id, annotator_id, ia_generated)
            VALUES (%s, %s, %s, %s);
        """
        expected_params = ("path/to/summary", 10, 5, True)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.summary_model.db_singleton")
    def test_update_summary_all_fields(self, mock_db_singleton):
        """Test mise à jour d'un résumé avec tous les champs."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        summary_model = SummaryModel()
        result = summary_model.update_summary(
            id_summary=1,
            path="updated/path",
            original_text_id=20,
            annotator_id=8,
            ia_generated=False
        )

        expected_query = """
            UPDATE summaries
            SET path = %s, original_text_id = %s, annotator_id = %s, ia_generated = %s
            WHERE id_summary = %s;
        """
        expected_params = ("updated/path", 20, 8, False, 1)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.summary_model.db_singleton")
    def test_update_summary_some_fields(self, mock_db_singleton):
        """Test mise à jour d'un résumé avec certains champs uniquement."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        summary_model = SummaryModel()
        result = summary_model.update_summary(
            id_summary=1,
            path="updated/path"
        )

        expected_query = """
            UPDATE summaries
            SET path = %s
            WHERE id_summary = %s;
        """
        expected_params = ("updated/path", 1)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.summary_model.db_singleton")
    def test_update_summary_no_updates(self, mock_db_singleton):
        """Test mise à jour sans modification."""
        mock_execute_query = MagicMock()
        mock_db_singleton.execute_query = mock_execute_query

        summary_model = SummaryModel()
        result = summary_model.update_summary(id_summary=1)

        mock_db_singleton.execute_query.assert_not_called()
        assert result is None

    @patch("flaskr.models.summary_model.db_singleton")
    def test_delete_summary(self, mock_db_singleton):
        """Test suppression d'un résumé."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        summary_model = SummaryModel()
        result = summary_model.delete_summary(id_summary=1)

        expected_query = "DELETE FROM summaries WHERE id_summary = %s;"
        expected_params = (1,)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"
