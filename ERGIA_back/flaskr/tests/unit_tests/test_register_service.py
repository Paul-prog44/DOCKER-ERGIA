import unittest
from unittest.mock import MagicMock, patch
from werkzeug.exceptions import BadRequest, Conflict
from flaskr.services.register_service import RegisterService
from flaskr.entities.users.create_user_request_dto import CreateUserRequestDTO

class TestExecCreateUser(unittest.TestCase):

    def setUp(self):
        # Initialisation du service et du mock du modèle utilisateur
        self.register_service = RegisterService()
        self.mock_user_model = MagicMock()
        self.register_service.user_model = self.mock_user_model

    def test_valid_user_creation(self):
        """Test de la création réussie d'un utilisateur."""
        # Données d'entrée valides
        register_data = CreateUserRequestDTO(
            email="test@example.com",
            password="ValidPassword1!",
            firstname="firstname",
            lastname="lastname",
            acceptCgu=True
        )

        # Configuration du mock
        self.mock_user_model.get_user_by_email.return_value = None  # Email disponible
        self.mock_user_model.create_user.return_value = [{"id_user": 1}]

        # Appel de la méthode et vérification du résultat
        user_id = self.register_service.exec_create_user(register_data)
        self.assertEqual(user_id, 1)
        self.mock_user_model.get_user_by_email.assert_called_once_with("test@example.com")
        self.mock_user_model.create_user.assert_called_once_with(register_data)

    def test_invalid_password_length(self):
        """Test de la validation du mot de passe avec une longueur insuffisante."""
        register_data = CreateUserRequestDTO(
            email="test@example.com",
            password="Short1!",
            firstname="firstname",
            lastname="lastname",
            acceptCgu=True
        )

        with self.assertRaises(BadRequest) as context:
            self.register_service.exec_create_user(register_data)
        self.assertIn("Mot de passe invalide", str(context.exception))

    def test_invalid_password_missing_uppercase(self):
        """Test de la validation du mot de passe sans lettre majuscule."""
        register_data = CreateUserRequestDTO(
            email="test@example.com",
            password="validpassword1!",
            firstname="firstname",
            lastname="lastname",
            acceptCgu=True
        )

        with self.assertRaises(BadRequest) as context:
            self.register_service.exec_create_user(register_data)
        self.assertIn("Mot de passe invalide", str(context.exception))

    def test_invalid_email_format(self):
        """Test de la validation du format d'email invalide."""
        register_data = CreateUserRequestDTO(
            email="invalid-email",
            password="ValidPassword1!",
            firstname="firstname",
            lastname="lastname",
            acceptCgu=True
        )

        with self.assertRaises(BadRequest) as context:
            self.register_service.exec_create_user(register_data)
        self.assertIn("Format du mail invalide", str(context.exception))

    def test_email_already_taken(self):
        """Test de la validation lorsqu'un email est déjà pris."""
        register_data = CreateUserRequestDTO(
            email="test@example.com",
            password="ValidPassword1!",
            firstname="firstname",
            lastname="lastname",
            acceptCgu=True
        )

        # Configuration du mock pour simuler un email existant
        self.mock_user_model.get_user_by_email.return_value = {"id_user": 1}

        with self.assertRaises(Conflict) as context:
            self.register_service.exec_create_user(register_data)
        self.assertIn("Un compte existe déjà à cet email", str(context.exception))
        self.mock_user_model.get_user_by_email.assert_called_once_with("test@example.com")

    def test_user_creation_failure(self):
        """Test de l'exception lors de l'échec de la création d'utilisateur."""
        register_data = CreateUserRequestDTO(
            email="test@example.com",
            password="ValidPassword1!",
            firstname="firstname",
            lastname="lastname",
            acceptCgu=True
        )

        # Configuration des mocks
        self.mock_user_model.get_user_by_email.return_value = None  # Email disponible
        self.mock_user_model.create_user.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.register_service.exec_create_user(register_data)
        self.assertIn("Database error", str(context.exception))
        self.mock_user_model.get_user_by_email.assert_called_once_with("test@example.com")
        self.mock_user_model.create_user.assert_called_once_with(register_data)

if __name__ == "__main__":
    unittest.main()
