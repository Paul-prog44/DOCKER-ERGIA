import pytest
from unittest.mock import MagicMock, patch
from werkzeug.exceptions import BadRequest
from flaskr.entities.users.login_request_dto import LoginRequestDTO
from flaskr.services.authentication_service import AuthenticationService
import os

os.environ['TESTING'] = 'True'


class TestAuthenticationService:

    def setup_method(self):
        # Mock du modèle utilisateur
        self.mock_user_model = MagicMock()
        self.auth_service = AuthenticationService()
        self.auth_service.user_model = self.mock_user_model  # Injection du modèle mocké

    def test_exec_login_valid_user(self):
        # Données simulées pour un utilisateur valide
        mock_user_data = [{
            "id_user": 1,
            "email": "test@example.com",
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # "password" en SHA256
        }]
        self.mock_user_model.get_user_by_email.return_value = mock_user_data

        # Créez un DTO valide
        login_data = LoginRequestDTO(email="test@example.com", password="password")

        # Appeler la méthode et vérifier le résultat
        user_data, status_code = self.auth_service.exec_login(login_data)
        assert status_code == 200
        assert user_data == mock_user_data

        # Vérifiez que la méthode mockée a été appelée correctement
        self.mock_user_model.get_user_by_email.assert_called_once_with("test@example.com")

    def test_exec_login_invalid_user(self):
        # Simulez l'absence d'utilisateur dans la base de données
        self.mock_user_model.get_user_by_email.return_value = None

        # Créez un DTO valide
        login_data = LoginRequestDTO(email="invalid@example.com", password="password")

        # Vérifiez qu'une exception est levée
        with pytest.raises(BadRequest, match="Identifiants incorrects"):
            self.auth_service.exec_login(login_data)

        # Vérifiez que la méthode mockée a été appelée correctement
        self.mock_user_model.get_user_by_email.assert_called_once_with("invalid@example.com")

    def test_exec_login_invalid_password(self):
        # Données simulées pour un utilisateur avec un mot de passe incorrect
        mock_user_data = [{
            "id_user": 1,
            "email": "test@example.com",
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd658d8fbf4e2d5d02c"  # "password" en SHA256
        }]
        self.mock_user_model.get_user_by_email.return_value = mock_user_data

        # Créez un DTO avec un mot de passe incorrect
        login_data = LoginRequestDTO(email="test@example.com", password="wrongpassword")

        # Vérifiez qu'une exception est levée
        with pytest.raises(BadRequest, match="Identifiants incorrects"):
            self.auth_service.exec_login(login_data)

        # Vérifiez que la méthode mockée a été appelée correctement
        self.mock_user_model.get_user_by_email.assert_called_once_with("test@example.com")
