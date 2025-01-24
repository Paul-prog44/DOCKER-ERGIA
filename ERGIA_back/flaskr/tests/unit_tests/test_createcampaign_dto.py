import unittest
from datetime import datetime
from pydantic import ValidationError
from flaskr.entities.campaigns.create_campaign_request_dto import CreateCampaignRequestDTO  # Remplacez par le chemin réel
import os

os.environ['TESTING'] = 'True'

class TestCreateCampaignRequestDTO(unittest.TestCase):

    def test_valid_dto(self):
        """Test avec des données valides."""
        payload = {
            "owner_id": 1,
            "date_phase_1": datetime(2024, 12, 28, 10, 30),
            "date_phase_2": datetime(2024, 12, 30, 15, 45),
            "name": "Test Campaign",
            "status_id": 2
        }
        dto = CreateCampaignRequestDTO(**payload)
        self.assertEqual(dto.owner_id, 1)
        self.assertEqual(dto.date_phase_1, datetime(2024, 12, 28, 10, 30))
        self.assertEqual(dto.date_phase_2, datetime(2024, 12, 30, 15, 45))
        self.assertEqual(dto.name, "Test Campaign")
        self.assertEqual(dto.status_id, 2)

    def test_optional_fields(self):
        """Test des champs optionnels non fournis."""
        payload = {
            "owner_id": 1,
            "name": "Test Campaign",
        }
        dto = CreateCampaignRequestDTO(**payload)
        self.assertEqual(dto.owner_id, 1)
        self.assertIsNone(dto.date_phase_1)  # Champ non fourni
        self.assertIsNone(dto.date_phase_2)  # Champ non fourni
        self.assertEqual(dto.name, "Test Campaign")
        self.assertEqual(dto.status_id, 1)  # Valeur par défaut

    def test_invalid_owner_id(self):
        """Test avec un `owner_id` invalide."""
        payload = {
            "owner_id": "not-an-int",
            "name": "Test Campaign",
        }
        with self.assertRaises(ValidationError) as context:
            CreateCampaignRequestDTO(**payload)
        self.assertIn("Input should be a valid integer", str(context.exception))

    def test_missing_name_field(self):
        """Test avec le champ `name` manquant."""
        payload = {
            "owner_id": 1,
        }
        with self.assertRaises(ValidationError) as context:
            CreateCampaignRequestDTO(**payload)
        self.assertIn("Field required", str(context.exception))

    def test_date_format_validation(self):
        """Test avec une date invalide."""
        payload = {
            "owner_id": 1,
            "date_phase_1": "invalid-date",
            "name": "Test Campaign",
        }
        with self.assertRaises(ValidationError) as context:
            CreateCampaignRequestDTO(**payload)
        self.assertIn("Input should be a valid datetime", str(context.exception))

    def test_json_serialization(self):
        """Test de la sérialisation JSON."""
        payload = {
            "owner_id": 1,
            "date_phase_1": datetime(2024, 12, 28, 10, 30),
            "date_phase_2": datetime(2024, 12, 30, 15, 45),
            "name": "Test Campaign",
            "status_id": 2
        }
        dto = CreateCampaignRequestDTO(**payload)
        json_data = dto.json()
        self.assertIn('"owner_id":1', json_data)
        self.assertIn('"name":"Test Campaign"', json_data)
        self.assertIn('"status_id":2', json_data)

if __name__ == '__main__':
    unittest.main()
