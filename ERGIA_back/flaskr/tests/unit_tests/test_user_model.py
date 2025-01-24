from unittest.mock import patch, MagicMock
import pytest
from flaskr.models.user_model import UserModel
from flaskr.entities.users.create_user_request_dto import CreateUserRequestDTO
from flaskr.entities.users.delete_user_request_dto import DeleteUserRequestDTO

class TestUserModel:

    @patch("flaskr.models.user_model.db_singleton")
    def test_get_all_users(self, mock_db_singleton):
        """Test récupération de tous les utilisateurs."""
        mock_execute_query = MagicMock(return_value=[{"id_user": 1, "lastname": "Doe", "firstname": "John", "email": "john.doe@example.com"}])
        mock_db_singleton.execute_query = mock_execute_query

        user_model = UserModel()
        result = user_model.get_all_users()

        expected_query = "SELECT * FROM users;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query)
        assert result == [{"id_user": 1, "lastname": "Doe", "firstname": "John", "email": "john.doe@example.com"}]

    @patch("flaskr.models.user_model.db_singleton")
    def test_get_user(self, mock_db_singleton):
        """Test récupération d'un utilisateur par ID."""
        mock_execute_query = MagicMock(return_value=[{"id_user": 1, "lastname": "Doe", "firstname": "John", "email": "john.doe@example.com"}])
        mock_db_singleton.execute_query = mock_execute_query

        user_model = UserModel()
        user_id = 1
        result = user_model.get_user(user_id)

        expected_query = "SELECT * FROM users WHERE id_user = %s;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, (user_id,))
        assert result == [{"id_user": 1, "lastname": "Doe", "firstname": "John", "email": "john.doe@example.com"}]

    @patch("flaskr.models.user_model.db_singleton")
    def test_get_user_by_email(self, mock_db_singleton):
        """Test récupération d'un utilisateur par email."""
        mock_execute_query = MagicMock(return_value=[{"id_user": 1, "lastname": "Doe", "firstname": "John", "email": "john.doe@example.com"}])
        mock_db_singleton.execute_query = mock_execute_query

        user_model = UserModel()
        email = "john.doe@example.com"
        result = user_model.get_user_by_email(email)

        expected_query = "SELECT * FROM users WHERE email = %s;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, (email,))
        assert result == [{"id_user": 1, "lastname": "Doe", "firstname": "John", "email": "john.doe@example.com"}]

    @patch("flaskr.models.user_model.db_singleton")
    def test_get_user_id_by_email(self, mock_db_singleton):
        """Test récupération de l'ID utilisateur par email."""
        mock_execute_query = MagicMock(return_value=[{"id_user": 1}])
        mock_db_singleton.execute_query = mock_execute_query

        user_model = UserModel()
        email = "john.doe@example.com"
        result = user_model.get_user_id_by_email(email)

        expected_query = "SELECT id_user FROM users WHERE email = %s;"
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, (email,))
        assert result == [{"id_user": 1}]

    @patch("flaskr.models.user_model.db_singleton")
    def test_create_user(self, mock_db_singleton):
        """Test création d'un utilisateur."""
        mock_execute_query = MagicMock(return_value=[{"id_user": 1}])
        mock_db_singleton.execute_query = mock_execute_query

        user_model = UserModel()
        register_data = CreateUserRequestDTO(
            lastname="Doe",
            firstname="John",
            email="john.doe@example.com",
            password="password123",
            acceptCgu=True
        )
        result = user_model.create_user(register_data)

        expected_query = """
            INSERT INTO users (lastname, firstname, email, password, accept_cgu)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_user;
        """
        expected_params = ("Doe", "John", "john.doe@example.com", "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f", True)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == [{"id_user": 1}]

    @patch("flaskr.models.user_model.db_singleton")
    def test_update_user(self, mock_db_singleton):
        """Test mise à jour d'un utilisateur."""
        
        # Mock de la méthode execute_query utilisée dans update_user
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query_for_put = mock_execute_query

        # Données d'entrée pour la mise à jour
        user_model = UserModel()
        result = user_model.update_user(
            user_id=1,
            lastname="Smith",
            firstname="Jane",
            email="jane.smith@example.com",
            password="newpassword123"
        )

        # Requête et paramètres attendus
        expected_query = """
            UPDATE users
            SET lastname = %s, firstname = %s, email = %s, password = %s
            WHERE id_user = %s;
        """
        expected_params = (
            "Smith", 
            "Jane", 
            "jane.smith@example.com", 
            "c822a0abf4ef0a5fc2a4c2010ed111e16af3ae95cee462a55e7877b8623ade36",  # sha256 du mot de passe
            1
        )
        
        # Vérification que la méthode execute_query a été appelée avec les bons paramètres
        mock_db_singleton.execute_query_for_put.assert_called_once_with(expected_query, expected_params)

        # Vérification que le résultat est celui attendu
        assert result == "Mocked Result"


    @patch("flaskr.models.user_model.db_singleton")
    def test_update_user_no_changes(self, mock_db_singleton):
        """Test mise à jour sans modification."""
        mock_execute_query = MagicMock()
        mock_db_singleton.execute_query = mock_execute_query

        user_model = UserModel()
        result = user_model.update_user(user_id=1)

        mock_db_singleton.execute_query.assert_not_called()
        assert result is None

    @patch("flaskr.models.user_model.db_singleton")
    def test_delete_user(self, mock_db_singleton):
        """Test suppression d'un utilisateur."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        user_model = UserModel()
        result = user_model.delete_user(user_id=1)

        expected_query = "DELETE FROM users WHERE id_user = %s;"
        expected_params = (1,)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"

    @patch("flaskr.models.user_model.db_singleton")
    def test_delete_user_by_email(self, mock_db_singleton):
        """Test suppression d'un utilisateur par email."""
        mock_execute_query = MagicMock(return_value="Mocked Result")
        mock_db_singleton.execute_query = mock_execute_query

        user_model = UserModel()
        delete_data = DeleteUserRequestDTO(email="john.doe@example.com")
        result = user_model.delete_user_by_email(delete_data)

        expected_query = "DELETE FROM users WHERE email = %s;"
        expected_params = ("john.doe@example.com",)
        mock_db_singleton.execute_query.assert_called_once_with(expected_query, expected_params)
        assert result == "Mocked Result"
