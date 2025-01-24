from unittest.mock import patch, MagicMock
import pytest
from flaskr.models.status_model import StatusModel

class TestStatusModel:

    @patch("flaskr.models.status_model.db_singleton")
    def test_get_all_statuses(self, mock_db_singleton):
        """Test récupération de tous les statuts."""
        mock_execute_query = MagicMock(return_value=[{"id_status": 1, "name": "Active"}])
        mock_db_singleton.execute_query = mock_execute_query

        status_model = StatusModel()
        result = status_model.get_all_statuses()

        expected_query = "SELECT * FROM statuses;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query)
        assert result == [{"id_status": 1, "name": "Active"}]

    @patch("flaskr.models.status_model.db_singleton")
    def test_get_status(self, mock_db_singleton):
        """Test récupération d'un statut par ID."""
        mock_execute_query = MagicMock(return_value={"id_status": 1, "name": "Active"})
        mock_db_singleton.execute_query = mock_execute_query

        status_model = StatusModel()
        id_status = 1
        result = status_model.get_status(id_status)

        expected_query = "SELECT * FROM statuses WHERE id_status = %s;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, (id_status,))
        assert result == {"id_status": 1, "name": "Active"}

    @patch("flaskr.models.status_model.db_singleton")
    def test_create_status(self, mock_db_singleton):
        """Test création d'un statut."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        status_model = StatusModel()
        result = status_model.create_status(name="New Status")

        expected_query = """
            INSERT INTO statuses (name)
            VALUES (%s);
        """
        expected_params = ("New Status",)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.status_model.db_singleton")
    def test_update_status_all_fields(self, mock_db_singleton):
        """Test mise à jour d'un statut avec un champ."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        status_model = StatusModel()
        result = status_model.update_status(id_status=1, name="Updated Status")

        expected_query = """
            UPDATE statuses
            SET name = %s
            WHERE id_status = %s;
        """
        expected_params = ("Updated Status", 1)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.status_model.db_singleton")
    def test_update_status_no_updates(self, mock_db_singleton):
        """Test mise à jour sans champ modifié."""
        mock_execute_query = MagicMock()
        mock_db_singleton.execute_query = mock_execute_query

        status_model = StatusModel()
        result = status_model.update_status(id_status=1)

        mock_db_singleton.execute_query.assert_not_called()
        assert result is None

    @patch("flaskr.models.status_model.db_singleton")
    def test_delete_status(self, mock_db_singleton):
        """Test suppression d'un statut."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        status_model = StatusModel()
        result = status_model.delete_status(id_status=1)

        expected_query = "DELETE FROM statuses WHERE id_status = %s;"
        expected_params = (1,)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"
