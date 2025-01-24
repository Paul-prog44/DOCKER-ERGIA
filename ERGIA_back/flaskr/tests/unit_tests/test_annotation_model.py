from unittest.mock import patch, MagicMock
import pytest

class TestAnnotationModel:

    
    @patch("flaskr.models.annotation_model.db_singleton")
    def test_get_all_annotations(self, mock_db_singleton):
        """Test récupération de toutes les annotations."""
        mock_execute_query = MagicMock(return_value=[{"id": 1, "name": "Annotation 1"}])
        mock_db_singleton.execute_query = mock_execute_query

        from flaskr.models.annotation_model import AnnotationModel

        annotation_model = AnnotationModel()
        result = annotation_model.get_all_annotations()

        expected_query = "SELECT * FROM annotations;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query)
        assert result == [{"id": 1, "name": "Annotation 1"}]

    @patch("flaskr.models.annotation_model.db_singleton")
    def test_get_annotation(self, mock_db_singleton):
        """Test récupération d'une annotation par ID."""
        mock_execute_query = MagicMock(return_value={"id": 1, "name": "Annotation 1"})
        mock_db_singleton.execute_query = mock_execute_query

        from flaskr.models.annotation_model import AnnotationModel

        annotation_model = AnnotationModel()
        id_annotation = 1
        result = annotation_model.get_annotation(id_annotation)

        expected_query = "SELECT * FROM annotations WHERE id_annotation = %s;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, (id_annotation,))
        assert result == {"id": 1, "name": "Annotation 1"}

    @patch("flaskr.models.annotation_model.db_singleton")
    def test_create_annotation(self, mock_db_singleton):
        """Test création d'une annotation."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        from flaskr.models.annotation_model import AnnotationModel

        annotation_model = AnnotationModel()
        result = annotation_model.create_annotation(
            scu_id=1, color="red", summary_id=10, index=5, length=15, creator="test_user"
        )

        expected_query = """
            INSERT INTO annotations (scu_id, color, summary_id, index, length, creator)
            VALUES (%s, %s, %s, %s, %s, %s) returning id_annotation;
        """
        expected_params = (1, "red", 10, 5, 15, "test_user")
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.annotation_model.db_singleton")
    def test_update_annotation_all_fields(self, mock_db_singleton):
        """Test mise à jour d'une annotation avec tous les champs."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        from flaskr.models.annotation_model import AnnotationModel

        annotation_model = AnnotationModel()
        result = annotation_model.update_annotation(
            id_annotation=1,
            scu_id=2,
            color="blue",
            summary_id=20,
            index=10,
            length=25,
            creator="new_user",
        )

        expected_query = """
            UPDATE annotations
            SET scu_id = %s, color = %s, summary_id = %s, index = %s, length = %s, creator = %s
            WHERE id_annotation = %s;
        """
        expected_params = (2, "blue", 20, 10, 25, "new_user", 1)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.annotation_model.db_singleton")
    def test_update_annotation_some_fields(self, mock_db_singleton):
        """Test mise à jour d'une annotation avec certains champs uniquement."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query
        
        from flaskr.models.annotation_model import AnnotationModel

        annotation_model = AnnotationModel()
        result = annotation_model.update_annotation(
            id_annotation=1,
            color="green",
            length=30,
        )

        expected_query = """
            UPDATE annotations
            SET color = %s, length = %s
            WHERE id_annotation = %s;
        """
        expected_params = ("green", 30, 1)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.annotation_model.db_singleton")
    def test_update_annotation_no_updates(self, mock_db_singleton):
        """Test mise à jour sans aucun champ modifié."""
        mock_execute_query = MagicMock()
        mock_db_singleton.execute_query = mock_execute_query

        from flaskr.models.annotation_model import AnnotationModel

        annotation_model = AnnotationModel()
        result = annotation_model.update_annotation(id_annotation=1)

        mock_db_singleton.execute_query.assert_not_called()
        assert result is None

    @patch("flaskr.models.annotation_model.db_singleton")
    def test_delete_annotation(self, mock_db_singleton):
        """Test suppression d'une annotation."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query
        
        from flaskr.models.annotation_model import AnnotationModel

        annotation_model = AnnotationModel()
        result = annotation_model.delete_annotation(id_annotation=1)

        expected_query = "DELETE FROM annotations WHERE id_annotation = %s;"
        expected_params = (1,)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"
