from unittest.mock import patch, MagicMock
import pytest
from flaskr.models.corpus_model import CorpusModel

class TestCorpusModel:

    @patch("flaskr.models.corpus_model.db_singleton")
    def test_get_all_texts(self, mock_db_singleton):
        """Test récupération de tous les textes."""
        mock_execute_query = MagicMock(return_value=[{"id_original_text": 1, "path": "some_path", "campaign_id": 1}])
        mock_db_singleton.execute_query = mock_execute_query

        corpus_model = CorpusModel()

        result = corpus_model.get_all_texts()

        expected_query = "SELECT * FROM original_texts;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query)
        assert result == [{"id_original_text": 1, "path": "some_path", "campaign_id": 1}]

    @patch("flaskr.models.corpus_model.db_singleton")
    def test_get_last_text(self, mock_db_singleton):
        """Test récupération du dernier texte."""
        mock_execute_query = MagicMock(return_value=[{"id_original_text": 1, "path": "some_path", "campaign_id": 1}])
        mock_db_singleton.execute_query = mock_execute_query

        corpus_model = CorpusModel()

        result = corpus_model.get_last_text()

        expected_query = "SELECT * FROM original_texts ORDER BY id_original_text DESC LIMIT 1;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query)
        assert result == [{"id_original_text": 1, "path": "some_path", "campaign_id": 1}]

    @patch("flaskr.models.corpus_model.db_singleton")
    def test_add_text(self, mock_db_singleton):
        """Test ajout d'un texte."""
        mock_execute_query = MagicMock(return_value=[{"id_original_text": 1}])
        mock_db_singleton.execute_query = mock_execute_query

        corpus_model = CorpusModel()

        path = "new_text_path"
        campaign_id = 1

        result = corpus_model.add_text(path, campaign_id)

        expected_query = "INSERT INTO original_texts (path, campaign_id) VALUES (%s, %s) returning id_original_text;"
        expected_params = (path, campaign_id)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == [{"id_original_text": 1}]

    @patch("flaskr.models.corpus_model.db_singleton")
    def test_add_summary(self, mock_db_singleton):
        """Test ajout d'un résumé."""
        mock_execute_query = MagicMock(return_value=[{"id_summary": 1}])
        mock_db_singleton.execute_query = mock_execute_query

        corpus_model = CorpusModel()

        path = "summary_path"
        text_id = 1
        ia_generated = True

        result = corpus_model.add_summary(path, text_id, ia_generated)

        expected_query = "INSERT INTO summaries (path, original_text_id, ia_generated) VALUES (%s, %s, %s) returning id_summary;"
        expected_params = (path, text_id, ia_generated)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == [{"id_summary": 1}]

    @patch("flaskr.models.corpus_model.db_singleton")
    def test_get_summary(self, mock_db_singleton):
        """Test récupération d'un résumé."""
        mock_execute_query = MagicMock(return_value=[{"id_summary": 1, "path": "summary_path", "original_text_id": 1, "ia_generated": True}])
        mock_db_singleton.execute_query = mock_execute_query

        corpus_model = CorpusModel()

        summary_id = 1

        result = corpus_model.get_summary(summary_id)

        expected_query = "SELECT * FROM summaries WHERE id_summary = %s;"
        expected_params = (summary_id,)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == [{"id_summary": 1, "path": "summary_path", "original_text_id": 1, "ia_generated": True}]

    @patch("flaskr.models.corpus_model.db_singleton")
    def test_get_text(self, mock_db_singleton):
        """Test récupération d'un texte spécifique."""
        mock_execute_query = MagicMock(return_value=[{"id_original_text": 1, "path": "some_path", "campaign_id": 1}])
        mock_db_singleton.execute_query = mock_execute_query

        corpus_model = CorpusModel()

        text_id = 1

        result = corpus_model.get_text(text_id)

        expected_query = "SELECT * FROM original_texts WHERE id_original_text = %s;"
        expected_params = (text_id,)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == [{"id_original_text": 1, "path": "some_path", "campaign_id": 1}]
